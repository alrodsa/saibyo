import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch
import numpy as np

from saibyo.utils.comparation.frame import frame_at_time, put_text


class TestFrameAtTime(unittest.TestCase):
    @patch("saibyo.utils.comparation.frame.cv2.VideoCapture")
    def test_returns_frame_when_success(self, mock_VideoCapture):
        cap = mock_VideoCapture.return_value
        fake_frame = np.ones((4, 6, 3), dtype=np.uint8)
        cap.read.return_value = (True, fake_frame)

        out = frame_at_time(cap, 1.23)

        cap.set.assert_called_once()
        args, _ = cap.set.call_args
        # cv2.CAP_PROP_POS_MSEC es el primer arg; el segundo debe ser 1230 ms
        self.assertEqual(len(args), 2)
        self.assertEqual(args[1], 1230.0)
        self.assertIs(out, fake_frame)

    @patch("saibyo.utils.comparation.frame.cv2.VideoCapture")
    def test_returns_none_when_failure(self, mock_VideoCapture):
        cap = mock_VideoCapture.return_value
        cap.read.return_value = (False, None)

        out = frame_at_time(cap, 0.5)

        self.assertIsNone(out)


class TestPutText(unittest.TestCase):
    def setUp(self):
        # fps no entero para verificar ceil()
        self.meta = SimpleNamespace(
            fps=24.2,
            width=200,
            height=100,
            input_path="/home/user/clip_demo.mp4",
        )
        self.blank = np.zeros((self.meta.height, self.meta.width, 3), dtype=np.uint8)

    @patch("saibyo.utils.comparation.frame.cv2.putText")
    def test_bottom_left_writes_two_lines_and_blends_bg(self, mock_putText):
        frame = self.blank.copy()
        out = put_text(frame, self.meta, "bottom_left")

        self.assertEqual(mock_putText.call_count, 2)

        first_text  = mock_putText.call_args_list[0].args[1]  # <- texto
        second_text = mock_putText.call_args_list[1].args[1]  # <- texto

        self.assertIn("25 FPS", first_text)
        self.assertIn("clip_demo.mp4", second_text)


    @patch("saibyo.utils.comparation.frame.cv2.putText")
    def test_top_right_uses_expected_strings(self, mock_putText):
        frame = self.blank.copy()
        out = put_text(frame, self.meta, "top_right")

        self.assertEqual(mock_putText.call_count, 2)

        texts = [c.args[1] for c in mock_putText.call_args_list]  # <- textos
        self.assertIn("25 FPS", texts[0])
        self.assertIn("clip_demo.mp4", texts[1])
