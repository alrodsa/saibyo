from unittest import TestCase
from unittest.mock import ANY, patch

from saibyo.conf.conf import SaibyoConf
from saibyo.core.interpolation.rife import RifeInterpolator


class TestCliInterpolate(TestCase):

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

    @patch("saibyo.cli.interpolate.RifeInterpolator.run", return_value=RifeInterpolator)
    @patch("saibyo.cli.interpolate.configure")
    def test_interpolate(self, mock_configure, mock_run):
        from saibyo.cli.interpolate import interpolate
        mock_configure.return_value = self.conf
        input_path = "/videos/input_video.mp4"
        output_folder = "/output_folder/"

        interpolate(input_path, output_folder)

        mock_configure.assert_called_once_with(
            "saibyo-lib", ANY, SaibyoConf
        )
        mock_run.assert_called_once_with(
            input_path=input_path, output_folder=output_folder
        )
