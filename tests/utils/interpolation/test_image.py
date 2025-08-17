import unittest

import torch

from saibyo.utils.interpolation.image import pad_to_multiple


class TestPadToMultiple(unittest.TestCase):
    def setUp(self) -> None:
        torch.manual_seed(0)

    def test_no_padding_when_already_multiple(self):
        img = torch.randn(3, 128, 64)  # 128 y 64 ya son múltiplos de 64
        out, h, w = pad_to_multiple(img, multiple=64)

        self.assertEqual(h, 128)
        self.assertEqual(w, 64)
        self.assertEqual(tuple(out.shape), (3, 128, 64))
        self.assertTrue(torch.equal(out, img))

    def test_padding_shape_and_zeros(self):
        img = torch.randn(3, 65, 66)  # no múltiplos de 64
        out, h, w = pad_to_multiple(img, multiple=64)

        # ph=128, pw=128 → padding bottom=63, right=62
        self.assertEqual((h, w), (65, 66))
        self.assertEqual(tuple(out.shape), (3, 128, 128))

        # Región original intacta
        self.assertTrue(torch.allclose(out[:, :h, :w], img))

        # Padding en borde inferior y derecho a 0
        self.assertTrue(torch.all(out[:, h:, :] == 0))
        self.assertTrue(torch.all(out[:, :, w:] == 0))

    def test_different_multiple(self):
        img = torch.randn(3, 10, 17)
        out, h, w = pad_to_multiple(img, multiple=8)
        # ph=((10-1)//8+1)*8=16, pw=((17-1)//8+1)*8=24
        self.assertEqual(tuple(out.shape), (3, 16, 24))
        self.assertEqual((h, w), (10, 17))

        self.assertTrue(torch.allclose(out[:, :h, :w], img))
        self.assertTrue(torch.all(out[:, h:, :] == 0))
        self.assertTrue(torch.all(out[:, :, w:] == 0))

    def test_multiple_one_keeps_shape(self):
        img = torch.randn(3, 13, 29)
        out, h, w = pad_to_multiple(img, multiple=1)
        self.assertEqual(tuple(out.shape), (3, 13, 29))
        self.assertTrue(torch.equal(out, img))
        self.assertEqual((h, w), (13, 29))

    def test_multiple_zero_raises(self):
        img = torch.randn(3, 5, 7)
        with self.assertRaises(ZeroDivisionError):
            pad_to_multiple(img, multiple=0)
