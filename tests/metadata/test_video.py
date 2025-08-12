import os
import unittest
from unittest.mock import patch, MagicMock

from saibyo.metadata.video import VideoMetadata


class TestVideoMetadata(unittest.TestCase):
    @patch("saibyo.metadata.video.Path.is_file", return_value=False)
    @patch("saibyo.metadata.video.Path.exists", return_value=False)
    def test_init_raises_when_path_not_exists(self, *_):
        with self.assertRaises(FileNotFoundError):
            VideoMetadata(input_path="/no/existe.mp4")

    @patch("saibyo.metadata.video.Path.is_file", return_value=False)
    @patch("saibyo.metadata.video.Path.exists", return_value=True)
    def test_init_raises_when_not_a_file(self, *_):
        with self.assertRaises(ValueError):
            VideoMetadata(input_path="/ruta/no_es_fichero")

    @patch("saibyo.metadata.video.cv2.VideoCapture")
    @patch("saibyo.metadata.video.Path.is_file", return_value=True)
    @patch("saibyo.metadata.video.Path.exists", return_value=True)
    def test_cached_properties_and_duration_seconds(
        self,
        mock_exists,         # <- Path.exists (decorador más cercano)
        mock_is_file,        # <- Path.is_file
        mock_VideoCapture,   # <- cv2.VideoCapture (decorador superior)
    ):
        cap = mock_VideoCapture.return_value
        def fake_get(prop):
            import cv2
            mapping = {
                cv2.CAP_PROP_FPS: 30.0,
                cv2.CAP_PROP_FRAME_COUNT: 300,
                cv2.CAP_PROP_FRAME_HEIGHT: 720,
                cv2.CAP_PROP_FRAME_WIDTH: 1280,
            }
            return mapping[prop]
        cap.get.side_effect = fake_get

        vm = VideoMetadata(input_path="/tmp/video.mp4")

        self.assertIs(vm.cap, cap)
        self.assertEqual(vm.fps, 30.0)
        self.assertEqual(vm.total_frames, 300)
        self.assertEqual(vm.height, 720)
        self.assertEqual(vm.width, 1280)
        self.assertEqual(vm.seconds, 10.0)
        self.assertEqual(vm.duration, "00:00:10")

        self.assertIs(vm.cap, cap)
        self.assertEqual(mock_VideoCapture.call_count, 1)

    @patch("saibyo.metadata.video.cv2.VideoCapture")
    @patch("saibyo.metadata.video.Path.is_file", return_value=True)
    @patch("saibyo.metadata.video.Path.exists", return_value=True)
    def test_info_logs_expected_message(self, mock_exists, mock_is_file, mock_VideoCapture):
        cap = mock_VideoCapture.return_value

        def fake_get(prop):
            import cv2
            mapping = {
                cv2.CAP_PROP_FPS: 24.2,
                cv2.CAP_PROP_FRAME_COUNT: 121,
                cv2.CAP_PROP_FRAME_HEIGHT: 1080,
                cv2.CAP_PROP_FRAME_WIDTH: 1920,
            }
            return mapping[prop]

        cap.get.side_effect = fake_get

        vm = VideoMetadata(input_path="/tmp/video.mp4")
        vm._logger = MagicMock()
        vm.info()

        args, _ = vm._logger.info.call_args
        msg = args[0]
        self.assertIn("Video Metadata", msg)
        self.assertIn("Video FPS: 25", msg)  # ceil(24.2)=25
        self.assertIn("Total Frames: 121", msg)
        self.assertIn("Height: 1080", msg)
        self.assertIn("Width: 1920", msg)
        self.assertIn("Duration: 00:00:05", msg)  # 121/24.2 = 5

    @patch("saibyo.metadata.video.cv2.VideoCapture")
    @patch("saibyo.metadata.video.Path.is_file", return_value=True)
    @patch("saibyo.metadata.video.Path.exists", return_value=True)
    def test_new_name_uses_multiplier_and_fps(self, mock_exists, mock_is_file, mock_VideoCapture):
        cap = mock_VideoCapture.return_value
        def fake_get(prop):
            import cv2
            mapping = {
                cv2.CAP_PROP_FPS: 30.0,
                cv2.CAP_PROP_FRAME_COUNT: 60,
                cv2.CAP_PROP_FRAME_HEIGHT: 720,
                cv2.CAP_PROP_FRAME_WIDTH: 1280,
            }
            return mapping[prop]
        cap.get.side_effect = fake_get

        vm = VideoMetadata(input_path="/home/user/video.mp4")
        self.assertEqual(vm.new_name(4), "video_x4_120fps.mp4")


    @patch("saibyo.metadata.video.cv2.VideoCapture")
    @patch("saibyo.metadata.video.Path.is_file", return_value=True)
    @patch("saibyo.metadata.video.Path.exists", return_value=True)
    def test_del_releases_capture_if_opened(self, mock_exists, mock_is_file, mock_VideoCapture):
        cap = mock_VideoCapture.return_value
        cap.get.side_effect = lambda *_: 30.0  # trigger cap creation
        cap.isOpened.return_value = True

        vm = VideoMetadata(input_path="/tmp/video.mp4")
        _ = vm.cap  # fuerza creación del cap (cached_property)
        VideoMetadata.__del__(vm)

        cap.isOpened.assert_called_once()
        cap.release.assert_called_once()

