import os
import tempfile
import unittest
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import MagicMock, patch

import numpy as np

from saibyo.conf.conf import SaibyoConf
from saibyo.engine.comparation.engine import ComparationEngine


class TestComparationEngine(TestCase):
    @patch.dict(
        os.environ,
        {
            "SAIBYO_COMPARATOR_OVERLAY_TEXT_OVERLAY": "True",
            "SAIBYO_COMPARATOR_OVERLAY_TEXT_POSITION": "top_left",
            "SAIBYO_COMPARATOR_BACKGROUND_COLOR": "#000000",
            "SAIBYO_COMPARATOR_MODE": "side_by_side",
            "SAIBYO_INTERPOLATOR_COMPARATION": "False",
            "SAIBYO_INTERPOLATOR_LIGHTWEIGHT": "True",
            "SAIBYO_INTERPOLATOR_EXPONENTIAL": "2",
        },
    )
    @patch("saibyo.engine.comparation.engine.Canvas.compose_on_canvas")
    @patch("saibyo.engine.comparation.engine.Canvas.add_overlay_text")
    @patch("saibyo.engine.comparation.engine.Canvas.create_canvas")
    @patch("saibyo.engine.comparation.engine.frame_at_time")
    @patch("saibyo.engine.comparation.engine.cv2.VideoWriter")
    @patch("saibyo.engine.comparation.engine.cv2.VideoCapture")
    @patch("saibyo.engine.comparation.engine.cv2.VideoWriter_fourcc")
    def test_compare_happy_path(
        self,
        mock_fourcc,
        mock_video_capture,
        mock_video_writer,
        mock_frame_at_time,
        mock_create_canvas,
        mock_add_overlay_text,
        mock_compose_on_canvas,
    ):
        conf = SaibyoConf().comparator
        engine = ComparationEngine(conf)

        video_a = SimpleNamespace(
            fps=24,
            seconds=1,
            input_path="/a.mp4",
            info=MagicMock(),
        )
        video_b = SimpleNamespace(
            fps=30,
            seconds=1,
            input_path="/b.mp4",
            info=MagicMock(),
        )

        mock_create_canvas.return_value = np.zeros((100, 200, 3), dtype=np.uint8)
        mock_frame_at_time.side_effect = [
            np.ones((50, 50, 3), dtype=np.uint8),
            np.ones((50, 50, 3), dtype=np.uint8),
        ] * 30
        mock_add_overlay_text.side_effect = lambda **kwargs: (
            kwargs["frame_a"],
            kwargs["frame_b"],
        )
        mock_compose_on_canvas.side_effect = lambda canvas, fa, fb, mode: canvas
        writer_instance = mock_video_writer.return_value

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "out.mp4")
            result = engine.compare(video_a, video_b, output_path)

        video_a.info.assert_called_once()
        video_b.info.assert_called_once()
        mock_create_canvas.assert_called_once()
        self.assertEqual(mock_video_capture.call_count, 2)
        self.assertTrue(mock_video_writer.called)
        self.assertTrue(writer_instance.write.called)
        self.assertTrue(writer_instance.release.called)
        self.assertIsInstance(result, np.ndarray)
