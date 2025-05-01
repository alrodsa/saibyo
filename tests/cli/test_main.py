from unittest import TestCase, mock
from unittest.mock import patch

from saibyo.cli.main import main


class TestMainCLI(TestCase):

    @patch("saibyo.cli.interpolate.interpolate", return_value=None)
    @patch("sys.argv", ["main.py", "interpolate", "input", "output"])
    @mock.patch("saibyo.cli.main.fire.Fire")
    def test_interpolate_command_called(self, mock_interpolate, _):
        main()
        mock_interpolate.assert_called_once()
