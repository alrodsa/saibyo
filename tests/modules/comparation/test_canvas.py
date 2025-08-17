import unittest
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np

from saibyo.modules.comparation.canvas import Canvas


class TestCanvas(unittest.TestCase):
    def setUp(self):
        self.va = SimpleNamespace(width=640, height=360)
        self.vb = SimpleNamespace(width=320, height=720)

    def test_dimensions_canvas(self):
        self.assertEqual(Canvas.dimensions_canvas(self.va, self.vb, "side_by_side"), (960, 720))
        self.assertEqual(Canvas.dimensions_canvas(self.va, self.vb, "top_bottom"), (640, 1080))
        self.assertEqual(Canvas.dimensions_canvas(self.va, self.vb, "split_half_vertical"), (640, 720))
        self.assertEqual(Canvas.dimensions_canvas(self.va, self.vb, "split_half_horizontal"), (640, 720))
        with self.assertRaises(ValueError):
            Canvas.dimensions_canvas(self.va, self.vb, "unknown")

    @patch("saibyo.modules.comparation.canvas.hex_to_rgb", return_value=(10, 20, 30))
    @patch.object(Canvas, "dimensions_canvas", return_value=(4, 3))
    def test_create_canvas(self, _, __):
        out = Canvas.create_canvas(self.va, self.vb, "side_by_side", "#0a141e")
        self.assertEqual(out.shape, (3, 4, 3))
        self.assertTrue(np.all(out == np.array([10, 20, 30], dtype=np.uint8)))

    @patch("saibyo.modules.comparation.canvas.put_text", side_effect=lambda frame, *_: frame)
    def test_add_overlay_text_calls_positions_side_by_side(self, mock_put):
        fa = np.zeros((2, 2, 3), dtype=np.uint8)
        fb = np.zeros((2, 2, 3), dtype=np.uint8)
        _ = Canvas.add_overlay_text(fa, fb, self.va, self.vb, "side_by_side")
        self.assertEqual(mock_put.call_count, 2)
        self.assertEqual(mock_put.call_args_list[0].args[2], "bottom_left")
        self.assertEqual(mock_put.call_args_list[1].args[2], "bottom_left")

    @patch("saibyo.modules.comparation.canvas.put_text", side_effect=lambda frame, *_: frame)
    def test_add_overlay_text_calls_positions_top_bottom(self, mock_put):
        fa = np.zeros((2, 2, 3), dtype=np.uint8)
        fb = np.zeros((2, 2, 3), dtype=np.uint8)
        _ = Canvas.add_overlay_text(fa, fb, self.va, self.vb, "top_bottom")
        self.assertEqual(mock_put.call_count, 2)
        self.assertEqual(mock_put.call_args_list[0].args[2], "bottom_left")
        self.assertEqual(mock_put.call_args_list[1].args[2], "bottom_left")

    @patch("saibyo.modules.comparation.canvas.put_text", side_effect=lambda frame, *_: frame)
    def test_add_overlay_text_calls_positions_split_vertical(self, mock_put):
        fa = np.zeros((2, 2, 3), dtype=np.uint8)
        fb = np.zeros((2, 2, 3), dtype=np.uint8)
        _ = Canvas.add_overlay_text(fa, fb, self.va, self.vb, "split_half_vertical")
        self.assertEqual(mock_put.call_count, 2)
        self.assertEqual(mock_put.call_args_list[0].args[2], "bottom_left")
        self.assertEqual(mock_put.call_args_list[1].args[2], "bottom_right")

    @patch("saibyo.modules.comparation.canvas.put_text", side_effect=lambda frame, *_: frame)
    def test_add_overlay_text_calls_positions_split_horizontal(self, mock_put):
        fa = np.zeros((2, 2, 3), dtype=np.uint8)
        fb = np.zeros((2, 2, 3), dtype=np.uint8)
        _ = Canvas.add_overlay_text(fa, fb, self.va, self.vb, "split_half_horizontal")
        self.assertEqual(mock_put.call_count, 2)
        self.assertEqual(mock_put.call_args_list[0].args[2], "top_left")
        self.assertEqual(mock_put.call_args_list[1].args[2], "bottom_left")

    def test_add_overlay_text_unsupported(self):
        fa = np.zeros((2, 2, 3), dtype=np.uint8)
        fb = np.zeros((2, 2, 3), dtype=np.uint8)
        with self.assertRaises(ValueError):
            Canvas.add_overlay_text(fa, fb, self.va, self.vb, "bad")

    def test_compose_on_canvas_side_by_side(self):
        canvas = np.zeros((10, 20, 3), dtype=np.uint8)
        fa = np.full((6, 8, 3), 50, dtype=np.uint8)
        fb = np.full((6, 8, 3), 200, dtype=np.uint8)
        out = Canvas.compose_on_canvas(canvas, fa, fb, "side_by_side")
        self.assertTrue(np.all(out[:, :10] == 50))
        self.assertTrue(np.all(out[:, 10:] == 200))

    def test_compose_on_canvas_top_bottom(self):
        canvas = np.zeros((10, 20, 3), dtype=np.uint8)
        fa = np.full((6, 8, 3), 60, dtype=np.uint8)
        fb = np.full((6, 8, 3), 180, dtype=np.uint8)
        out = Canvas.compose_on_canvas(canvas, fa, fb, "top_bottom")
        self.assertTrue(np.all(out[:5, :] == 60))
        self.assertTrue(np.all(out[5:, :] == 180))

    def test_compose_on_canvas_split_half_vertical(self):
        canvas = np.zeros((10, 20, 3), dtype=np.uint8)
        fa = np.full((6, 8, 3), 10, dtype=np.uint8)
        fb = np.full((6, 8, 3), 200, dtype=np.uint8)
        out = Canvas.compose_on_canvas(canvas, fa, fb, "split_half_vertical")
        self.assertTrue(np.all(out[:, :10] == 10))
        self.assertTrue(np.all(out[:, 11:] == 200))
        self.assertTrue(np.all(out[:, 10] == 255))

    def test_compose_on_canvas_split_half_horizontal(self):
        canvas = np.zeros((10, 20, 3), dtype=np.uint8)
        fa = np.full((6, 8, 3), 15, dtype=np.uint8)
        fb = np.full((6, 8, 3), 240, dtype=np.uint8)
        out = Canvas.compose_on_canvas(canvas, fa, fb, "split_half_horizontal")
        self.assertTrue(np.all(out[:5, :] == 15))
        self.assertTrue(np.all(out[6:, :] == 240))
        self.assertTrue(np.all(out[5, :] == 255))

    def test_compose_on_canvas_unsupported(self):
        canvas = np.zeros((2, 2, 3), dtype=np.uint8)
        fa = np.zeros((1, 1, 3), dtype=np.uint8)
        fb = np.zeros((1, 1, 3), dtype=np.uint8)
        with self.assertRaises(ValueError):
            Canvas.compose_on_canvas(canvas, fa, fb, "nope")
