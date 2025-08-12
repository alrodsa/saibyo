import unittest

import torch
import torch.nn as nn

from saibyo.modules.interpolation import ifnet as ifm


class TestIFNetUtils(unittest.TestCase):
    def setUp(self) -> None:
        torch.manual_seed(0)

    def test_warp_identity_and_cache(self):
        ifm.backwarp_grid_cache.clear()
        device = torch.device("cpu")
        x = torch.randn(1, 3, 5, 7)
        flow = torch.zeros(1, 2, 5, 7)

        y1 = ifm.warp(x, flow, device)
        self.assertTrue(torch.allclose(y1, x, atol=1e-6))

        self.assertEqual(len(ifm.backwarp_grid_cache), 1)
        key = list(ifm.backwarp_grid_cache.keys())[0]
        grid_ref = ifm.backwarp_grid_cache[key]

        y2 = ifm.warp(x, flow, device)
        self.assertTrue(torch.allclose(y2, x, atol=1e-6))
        self.assertIs(ifm.backwarp_grid_cache[key], grid_ref)

    def test_conv_and_conv_bn_modules(self):
        m1 = ifm.conv(3, 8, kernel_size=3, stride=1, padding=1)
        self.assertIsInstance(m1, nn.Sequential)
        self.assertIsInstance(m1[0], nn.Conv2d)
        self.assertTrue(m1[0].bias is not None)
        self.assertIsInstance(m1[1], nn.LeakyReLU)
        out1 = m1(torch.randn(2, 3, 11, 13))
        self.assertEqual(tuple(out1.shape), (2, 8, 11, 13))

        m2 = ifm.conv_bn(3, 8, kernel_size=3, stride=1, padding=1)
        self.assertIsInstance(m2[0], nn.Conv2d)
        self.assertIsNone(m2[0].bias)
        self.assertIsInstance(m2[1], nn.BatchNorm2d)
        self.assertIsInstance(m2[2], nn.LeakyReLU)
        out2 = m2(torch.randn(2, 3, 11, 13))
        self.assertEqual(tuple(out2.shape), (2, 8, 11, 13))


class TestHeadResConv(unittest.TestCase):
    def setUp(self) -> None:
        torch.manual_seed(0)

    def test_head_forward_and_feat(self):
        head = ifm.Head()
        x = torch.randn(1, 3, 16, 16)
        y = head(x)
        self.assertEqual(tuple(y.shape), (1, 4, 16, 16))

        feats = head(x, feat=True)
        self.assertEqual(len(feats), 4)
        self.assertEqual(tuple(feats[0].shape), (1, 16, 8, 8))
        self.assertEqual(tuple(feats[1].shape), (1, 16, 8, 8))
        self.assertEqual(tuple(feats[2].shape), (1, 16, 8, 8))
        self.assertEqual(tuple(feats[3].shape), (1, 4, 16, 16))

    def test_resconv_identity_when_beta_zero_and_positive_input(self):
        layer = ifm.ResConv(8)
        with torch.no_grad():
            layer.beta.zero_()
        x = torch.ones(2, 8, 5, 7)  # positivo -> ReLU(x) = x
        y = layer(x)
        self.assertTrue(torch.allclose(y, x, atol=1e-6))
        self.assertEqual(tuple(y.shape), tuple(x.shape))


class TestIFBlock(unittest.TestCase):
    def setUp(self) -> None:
        torch.manual_seed(0)

    def test_ifblock_shapes_no_flow_scale1(self):
        block = ifm.IFBlock(in_channels=15, c=64)
        x = torch.randn(1, 15, 32, 32)
        flow, mask, feat = block(x, flow=None, scale=1)
        self.assertEqual(tuple(flow.shape), (1, 4, 32, 32))
        self.assertEqual(tuple(mask.shape), (1, 1, 32, 32))
        self.assertEqual(tuple(feat.shape), (1, 8, 32, 32))

    def test_ifblock_shapes_with_scale2_and_flow(self):
        block = ifm.IFBlock(in_channels=19, c=64)
        x = torch.randn(1, 15, 32, 32)
        prev_flow = torch.randn(1, 4, 32, 32)
        flow, mask, feat = block(x, flow=prev_flow, scale=2)
        self.assertEqual(tuple(flow.shape), (1, 4, 32, 32))
        self.assertEqual(tuple(mask.shape), (1, 1, 32, 32))
        self.assertEqual(tuple(feat.shape), (1, 8, 32, 32))


class TestIFNet(unittest.TestCase):
    def setUp(self) -> None:
        torch.manual_seed(0)

    def test_ifnet_forward_shapes(self):
        device = torch.device("cpu")
        net = ifm.IFNet(device=device)
        x = torch.randn(1, 6, 16, 16)

        # Mantén las dimensiones constantes en todo el forward
        scale_list = (1, 1, 1, 1, 1)

        flows, mask, merged = net(x, timestep=0.5, scale_list=scale_list, ensemble=False)

        self.assertEqual(len(flows), 5)
        for f in flows:
            self.assertEqual(tuple(f.shape), (1, 4, 16, 16))

        self.assertEqual(tuple(mask.shape), (1, 1, 16, 16))

        self.assertEqual(len(merged), 5)
        for i in range(4):
            self.assertIsInstance(merged[i], tuple)
            self.assertEqual(len(merged[i]), 2)
            self.assertEqual(tuple(merged[i][0].shape), (1, 3, 16, 16))
            self.assertEqual(tuple(merged[i][1].shape), (1, 3, 16, 16))
        self.assertIsInstance(merged[4], torch.Tensor)
        self.assertEqual(tuple(merged[4].shape), (1, 3, 16, 16))

