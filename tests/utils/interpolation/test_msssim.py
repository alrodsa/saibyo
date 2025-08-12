import unittest

import torch

from saibyo.utils.interpolation.msssim import create_window_3d, gaussian, ssim_matlab


class TestGaussianAndWindow(unittest.TestCase):
    def test_gaussian_properties(self):
        ws = 11
        g = gaussian(ws, sigma=1.5)
        self.assertEqual(g.ndim, 1)
        self.assertEqual(g.shape[0], ws)
        self.assertAlmostEqual(float(g.sum()), 1.0, places=6)
        self.assertTrue(torch.all(g >= 0))
        self.assertTrue(torch.allclose(g, torch.flip(g, dims=[0]), atol=1e-6))

    def test_create_window_3d_shape_and_sum(self):
        ws, ch = 7, 3
        w3d = create_window_3d(ws, channel=ch)
        self.assertEqual(tuple(w3d.shape), (1, ch, ws, ws, ws))
        self.assertAlmostEqual(float(w3d[0, 0].sum()), 1.0, places=5)
        self.assertAlmostEqual(float(w3d[0, ch - 1].sum()), 1.0, places=5)


class TestSSIMMatlab(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(0)

    def test_identical_images_ssim_is_one(self):
        x = torch.rand(1, 3, 16, 16)
        y = x.clone()
        s = ssim_matlab(x, y, window_size=11)
        self.assertIsInstance(s, torch.Tensor)
        self.assertAlmostEqual(float(s), 1.0, places=4)

    def test_different_images_low_ssim(self):
        x = torch.zeros(1, 3, 16, 16)
        y = torch.ones(1, 3, 16, 16)
        s = ssim_matlab(x, y, window_size=11)
        self.assertGreaterEqual(float(s), -1.0)
        self.assertLessEqual(float(s), 1.0)
        self.assertLess(float(s), 0.5)

    def test_size_average_false_shape(self):
        x = torch.rand(1, 3, 16, 16)
        y = torch.rand(1, 3, 16, 16)
        s = ssim_matlab(x, y, window_size=11, size_average=False)
        self.assertEqual(tuple(s.shape), (1, 16))
        self.assertTrue(torch.all(s <= 1.0))
        self.assertTrue(torch.all(s >= -1.0))

    def test_val_range_inference_matches_explicit_for_unit_range(self):
        x = torch.rand(1, 3, 16, 16)  # in [0,1]
        y = torch.rand(1, 3, 16, 16)
        s_auto = ssim_matlab(x, y, window_size=11, val_range=None)
        s_exp = ssim_matlab(x, y, window_size=11, val_range=1)
        self.assertAlmostEqual(float(s_auto), float(s_exp), places=6)

    def test_val_range_inference_matches_explicit_for_255_range(self):
        x = (torch.rand(1, 3, 16, 16) * 255.0)
        y = (torch.rand(1, 3, 16, 16) * 255.0)
        s_auto = ssim_matlab(x, y, window_size=11, val_range=None)
        s_exp = ssim_matlab(x, y, window_size=11, val_range=255)
        self.assertAlmostEqual(float(s_auto), float(s_exp), places=6)

    def test_large_window_clipped_to_image_size(self):
        x = torch.rand(1, 8, 16, 16)  # C=8  -> D tras pad = 18
        y = torch.rand(1, 8, 16, 16)
        s = ssim_matlab(x, y, window_size=31)  # 31 > 16, se recorta a 16
        self.assertTrue(-1.0 <= float(s) <= 1.0)


