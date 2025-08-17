from unittest import TestCase
from unittest.mock import patch

from saibyo.cli.main import main


class TestCliMain(TestCase):
    def setUp(self) -> None:
        super().setUp()

    @patch("saibyo.cli.main.interpolate")
    @patch("saibyo.cli.main.compare")
    @patch("fire.Fire")
    def test_cli_main_interpolate(self, mock_fire, mock_compare, mock_interpolate):
        main()

        mock_fire.assert_called_once()
        (arg_dict,), kwargs = mock_fire.call_args

        self.assertIsInstance(arg_dict, dict)
        self.assertIn("interpolate", arg_dict)
        self.assertIn("compare", arg_dict)
        self.assertIs(arg_dict["interpolate"], mock_interpolate)
        self.assertIs(arg_dict["compare"], mock_compare)
        self.assertEqual(kwargs, {})

