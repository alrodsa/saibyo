import tempfile
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from saibyo.conf.conf import SaibyoConf
from saibyo.core.interpolation.rife import RifeInterpolator


class TestRifeInterpolator(TestCase):
    @patch.dict(
        "os.environ",
        {
            "SAIBYO_INTERPOLATOR_COMPARATION": "False",
            "SAIBYO_INTERPOLATOR_LIGHTWEIGHT": "True",
            "SAIBYO_INTERPOLATOR_EXPONENTIAL": "3",
            "SAIBYO_COMPARATOR_OVERLAY_TEXT_OVERLAY": "True",
            "SAIBYO_COMPARATOR_OVERLAY_TEXT_POSITION": "top_left",
            "SAIBYO_COMPARATOR_BACKGROUND_COLOR": "#000000",
            "SAIBYO_COMPARATOR_MODE": "side_by_side"
        }
    )
    def setUp(self):
        super().setUp()
        self.conf = SaibyoConf()
        self.interpolator = RifeInterpolator(conf=self.conf)
        self.output_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        super().tearDown()
        self.output_dir.cleanup()

    @patch("saibyo.core.interpolation.rife.transfer_audio")
    @patch("saibyo.core.interpolation.rife.VideoIOManager")
    @patch("saibyo.core.interpolation.rife.RifeEngine")
    @patch("saibyo.core.interpolation.rife.VideoMetadata")
    def test_run_happy_path(
        self,
        mock_video_metadata,
        mock_rife_engine,
        mock_video_io_manager,
        mock_transfer_audio,
    ):
        input_path = "/videos/input.mp4"

        vm = mock_video_metadata.return_value
        vm.fps = 25
        vm.total_frames = 79
        vm.input_path = input_path
        vm.new_name.return_value = "input_x8_200fps.mp4"
        vm.info.return_value = None

        engine_instance = mock_rife_engine.return_value
        engine_instance.run.return_value = None

        result = self.interpolator.run(input_path=input_path, output_folder=self.output_dir.name)

        mock_video_metadata.assert_called_with(input_path=input_path)
        vm.info.assert_called_once()

        expected_multiplier = 8
        expected_boosted_fps = vm.fps * expected_multiplier
        expected_output_path = Path(self.output_dir.name) / vm.new_name.return_value

        self.assertTrue(mock_video_io_manager.called)
        _, vio_kwargs = mock_video_io_manager.call_args
        self.assertIs(vio_kwargs["video"], vm)
        self.assertEqual(vio_kwargs["fps"], expected_boosted_fps)
        self.assertEqual(vio_kwargs["output_path"], str(expected_output_path))

        self.assertTrue(mock_rife_engine.called)
        _, rife_kwargs = mock_rife_engine.call_args
        self.assertIs(rife_kwargs["conf"], self.conf)
        self.assertIs(rife_kwargs["io_manager"], mock_video_io_manager.return_value)
        self.assertEqual(rife_kwargs["total_frames"], vm.total_frames)

        engine_instance.run.assert_called_once_with()

        mock_transfer_audio.assert_called_once()
        ta_kwargs = mock_transfer_audio.call_args.kwargs
        self.assertEqual(ta_kwargs["source_video"], vm.input_path)
        self.assertEqual(Path(ta_kwargs["target_video"]), expected_output_path)

        self.assertIs(result, self.interpolator)
