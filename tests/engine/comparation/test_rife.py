import os
import unittest
from unittest.mock import patch, MagicMock

import torch
import numpy as np

from saibyo.engine.interpolation.rife import RifeModel


class TestRifeModel(unittest.TestCase):
    @patch.dict(
        os.environ,
        {
            "SAIBYO_INTERPOLATOR_COMPARATION": "False",
            "SAIBYO_INTERPOLATOR_LIGHTWEIGHT": "False",
            "SAIBYO_INTERPOLATOR_EXPONENTIAL": "2",
        },
        clear=False,
    )
    @patch("saibyo.engine.interpolation.rife.IFNet")
    @patch("saibyo.engine.interpolation.rife.torch.cuda.is_available", return_value=False)
    def test_init_constructs_ifnet_on_cpu(self, _, mock_IFNet):
        mock_IFNet.return_value.to.return_value = mock_IFNet.return_value
        model = RifeModel()
        mock_IFNet.assert_called_once()
        args, kwargs = mock_IFNet.call_args
        self.assertEqual(args[0].type, "cpu")
        mock_IFNet.return_value.to.assert_called_once()
        to_args, _ = mock_IFNet.return_value.to.call_args
        self.assertEqual(to_args[0].type, "cpu")
        self.assertEqual(model._device.type, "cpu")

    @patch("saibyo.engine.interpolation.rife.torch.load")
    @patch("saibyo.engine.interpolation.rife.IFNet")
    @patch("saibyo.engine.interpolation.rife.torch.cuda.is_available", return_value=False)
    def test_load_calls_torch_load_and_load_state_dict(self, _, mock_IFNet, mock_torch_load):
        mock_IFNet.return_value.to.return_value = mock_IFNet.return_value
        mock_torch_load.return_value = {"w": 1}
        model = RifeModel()
        out = model.load("/weights/dir")
        self.assertIs(out, model)
        mock_torch_load.assert_called_once()
        _, kwargs = mock_torch_load.call_args
        self.assertEqual(kwargs["map_location"].type, "cpu")
        mock_IFNet.return_value.load_state_dict.assert_called_once()
        ld_args, ld_kwargs = mock_IFNet.return_value.load_state_dict.call_args
        self.assertEqual(ld_kwargs["strict"], False)
        self.assertEqual(ld_args[0], {"w": 1})

    @patch("saibyo.engine.interpolation.rife.IFNet")
    @patch("saibyo.engine.interpolation.rife.torch.cuda.is_available", return_value=False)
    def test_eval_and_inference_flow(self, _, mock_IFNet):
        mock_IFNet.return_value.to.return_value = mock_IFNet.return_value
        model = RifeModel()
        out = model.eval()
        self.assertIs(out, model)
        mock_IFNet.return_value.eval.assert_called_once()

        merged0 = torch.randn(1, 3, 4, 6)
        merged1 = torch.randn(1, 3, 4, 6)
        mock_IFNet.return_value.side_effect = lambda imgs, t, scales: (None, None, [merged0, merged1])

        img0 = torch.zeros(1, 3, 4, 6, dtype=torch.float32)
        img1 = torch.ones(1, 3, 4, 6, dtype=torch.float32)
        timestep = 0.25
        scale = 2.0
        result = model.inference(img0, img1, timestep=timestep, scale=scale)

        call_args, call_kwargs = mock_IFNet.return_value.call_args
        self.assertIsInstance(call_args[0], torch.Tensor)
        self.assertEqual(call_args[0].shape, (1, 6, 4, 6))
        self.assertAlmostEqual(call_args[1], timestep)
        expected_scales = [16/scale, 8/scale, 4/scale, 2/scale, 1/scale]
        self.assertEqual(call_args[2], expected_scales)
        self.assertIs(result, merged1)
