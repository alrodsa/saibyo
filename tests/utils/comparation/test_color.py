import unittest

from saibyo.utils.comparation.color import hex_to_rgb


class TestHexToRgb(unittest.TestCase):
    def test_valid_uppercase(self):
        self.assertEqual(hex_to_rgb("#FF5733"), (255, 87, 51))

    def test_valid_lowercase(self):
        self.assertEqual(hex_to_rgb("#00ff00"), (0, 255, 0))

    def test_without_hash_prefix(self):
        self.assertEqual(hex_to_rgb("abcdef"), (171, 205, 239))

    def test_boundary_black(self):
        self.assertEqual(hex_to_rgb("#000000"), (0, 0, 0))

    def test_boundary_white(self):
        self.assertEqual(hex_to_rgb("#ffffff"), (255, 255, 255))

    def test_invalid_length_short(self):
        with self.assertRaises(ValueError) as ctx:
            hex_to_rgb("#123")
        self.assertIn("Invalid color", str(ctx.exception))

    def test_invalid_length_long(self):
        with self.assertRaises(ValueError) as ctx:
            hex_to_rgb("#1234567")
        self.assertIn("Invalid color", str(ctx.exception))

    def test_invalid_characters(self):
        with self.assertRaises(ValueError):
            hex_to_rgb("#GG0000")
        with self.assertRaises(ValueError):
            hex_to_rgb("ZZZZZZ")
