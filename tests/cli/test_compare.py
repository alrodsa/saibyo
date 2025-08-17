from unittest import TestCase
from unittest.mock import ANY, patch

from saibyo.conf.conf import SaibyoConf


class TestCliCompare(TestCase):
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
    def setUp(self) -> None:
        super().setUp()
        self.conf = SaibyoConf()

    @patch("saibyo.cli.compare.configure")
    @patch("saibyo.cli.compare.Comparator.compare")
    def test_compare(self, mock_compare, mock_configure):
        from saibyo.cli.compare import compare
        mock_configure.return_value = self.conf
        video_a = "/videos/input_video_a.mp4"
        video_b = "/videos/input_video_b.mp4"
        output_path = "/output_folder/"

        compare(video_a, video_b, output_path)

        mock_configure.assert_called_once_with("saibyo-lib", ANY, SaibyoConf)
        mock_compare.assert_called_once_with(video_a, video_b, output_path)
