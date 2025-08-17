import os
import unittest
from queue import Queue
from unittest.mock import patch, MagicMock

import numpy as np
import torch

from saibyo.conf.conf import SaibyoConf
from saibyo.engine.interpolation.engine import RifeEngine


class FakeIOManager:
    def __init__(self, frames):
        self.read_buffer = Queue()
        for f in frames:
            self.read_buffer.put(f)
        self.write_buffer = Queue()
        self.finished = False

    def finish(self):
        self.finished = True


class TestRifeEngine(unittest.TestCase):
    @patch.dict(
        os.environ,
        {
            "SAIBYO_INTERPOLATOR_COMPARATION": "False",
            "SAIBYO_INTERPOLATOR_LIGHTWEIGHT": "False",
            "SAIBYO_INTERPOLATOR_EXPONENTIAL": "2",  # multiplier = 4
        },
        clear=False,
    )
    @patch("saibyo.engine.interpolation.engine.ssim_matlab", return_value=0.5)
    @patch("saibyo.engine.interpolation.engine.tqdm")
    @patch("saibyo.engine.interpolation.engine.RifeModel")
    def test_run_basic_flow_mid_ssim_uses_make_inference(
        self, mock_rife_model, mock_tqdm, mock_ssim
    ):
        conf = SaibyoConf()

        h, w = 4, 6
        lastframe = np.full((h, w, 3), 10, dtype=np.uint8)
        nextframe = np.full((h, w, 3), 20, dtype=np.uint8)
        frames = [lastframe, nextframe, None]
        io = FakeIOManager(frames)

        mock_tqdm.return_value = MagicMock(update=MagicMock(), close=MagicMock())

        engine = RifeEngine(conf=conf, io_manager=io, total_frames=2)

        with patch.object(
            RifeEngine,
            "_make_inference",
            return_value=[
                torch.zeros((1, 3, h, w), dtype=torch.float32) for _ in range(3)
            ],
        ) as mock_make_inf:
            engine.run()

        self.assertTrue(io.finished)

        written = []
        while not io.write_buffer.empty():
            written.append(io.write_buffer.get())

        self.assertEqual(len(written), 5)
        self.assertTrue(np.array_equal(written[0], lastframe))
        self.assertEqual(written[1].shape, (h, w, 3))
        self.assertEqual(written[2].shape, (h, w, 3))
        self.assertEqual(written[3].shape, (h, w, 3))
        self.assertEqual(written[4].shape, (h, w, 3))

        self.assertEqual(mock_make_inf.call_count, 1)
        args, kwargs = mock_make_inf.call_args
        self.assertIsInstance(args[0], torch.Tensor)
        self.assertIsInstance(args[1], torch.Tensor)
        self.assertEqual(kwargs, {})

        mock_rife_model.assert_called_once()
        mock_rife_model.return_value.load.assert_called_once()

        mock_tqdm.return_value.update.assert_called()
        mock_tqdm.return_value.close.assert_called_once()

