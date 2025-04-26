import sys
import unittest
from unittest import mock
from unittest.mock import patch

from src.cli.main import main


class TestMainCLI(unittest.TestCase):

    @patch("src.cli.interpolate.interpolate", return_value=None)
    @patch("sys.argv", ["main.py", "interpolate", "input", "output"])
    @mock.patch("src.cli.main.fire.Fire")
    def test_interpolate_command_called(self, mock_interpolate, _):
        main()
        mock_interpolate.assert_called_once()
