from unittest import TestCase

import torch

from saibyo.utils.image import pad_to_multiple


class TestPadToMultiple(TestCase):

    def test_pad_smaller_image(self):
        img = torch.randn(3, 50, 50)
        padded_img, h, w = pad_to_multiple(img, multiple=64)

        self.assertEqual(h, 50)
        self.assertEqual(w, 50)
        self.assertEqual(padded_img.shape[1], 64)
        self.assertEqual(padded_img.shape[2], 64)

    def test_pad_larger_image(self):
        img = torch.randn(3, 128, 70)
        padded_img, h, w = pad_to_multiple(img, multiple=64)

        self.assertEqual(h, 128)
        self.assertEqual(w, 70)
        self.assertEqual(padded_img.shape[1], 128)
        self.assertEqual(padded_img.shape[2], 128)

    def test_pad_exact_multiple(self):
        img = torch.randn(3, 64, 64)
        padded_img, h, w = pad_to_multiple(img, multiple=64)

        self.assertEqual(padded_img.shape[1], 64)
        self.assertEqual(padded_img.shape[2], 64)

    def test_pad_custom_multiple(self):
        img = torch.randn(3, 45, 45)
        padded_img, _, _ = pad_to_multiple(img, multiple=32)

        self.assertEqual(padded_img.shape[1], 64)  # next multiple of 32 after 45
        self.assertEqual(padded_img.shape[2], 64)

