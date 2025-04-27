from unittest import TestCase

import torch

from src.modules.warplayer import backwarp_grid_cache, warp


class TestWarpFunction(TestCase):

    def setUp(self):
        backwarp_grid_cache.clear()

    def test_warp_basic(self):
        device = torch.device("cpu")

        input_tensor = torch.randn(1, 3, 32, 32, device=device)
        flow_tensor = torch.randn(1, 2, 32, 32, device=device)

        output = warp(input_tensor, flow_tensor, device=device)

        self.assertIsInstance(output, torch.Tensor)
        self.assertEqual(output.shape, input_tensor.shape)

    def test_warp_multiple_calls_uses_cache(self):
        device = torch.device("cpu")

        input_tensor = torch.randn(1, 3, 32, 32, device=device)
        flow_tensor = torch.randn(1, 2, 32, 32, device=device)

        warp(input_tensor, flow_tensor, device=device)

        cache_size_after_first = len(backwarp_grid_cache)

        warp(input_tensor, flow_tensor, device=device)

        self.assertEqual(len(backwarp_grid_cache), cache_size_after_first)

