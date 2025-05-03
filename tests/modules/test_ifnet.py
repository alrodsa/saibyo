import sys
from io import StringIO
from unittest import TestCase

import torch
from torch import nn

from saibyo.modules.ifnet import Head, IFBlock, IFNet, ResConv, conv_bn


class TestConvBn(TestCase):
    def test_conv_bn_structure_and_forward(self):
        in_channels = 3
        out_channels = 16
        module = conv_bn(in_channels, out_channels)

        self.assertIsInstance(module, nn.Sequential)
        self.assertEqual(len(module), 3)
        self.assertIsInstance(module[0], nn.Conv2d)
        self.assertIsInstance(module[1], nn.BatchNorm2d)
        self.assertIsInstance(module[2], nn.LeakyReLU)
        self.assertEqual(module[0].in_channels, in_channels)
        self.assertEqual(module[0].out_channels, out_channels)
        self.assertEqual(module[1].num_features, out_channels)

        input_tensor = torch.randn(1, in_channels, 64, 64)  # batch, channels, height, width
        output = module(input_tensor)

        self.assertEqual(output.shape[0], 1)
        self.assertEqual(output.shape[1], out_channels)
        self.assertEqual(output.shape[2], 64)
        self.assertEqual(output.shape[3], 64)

class TestHead(TestCase):
    def test_forward_output_shape(self):
        head = Head()
        input_tensor = torch.randn(1, 3, 64, 64)

        output = head(input_tensor)

        self.assertEqual(output.shape, (1, 4, 64, 64))

    def test_forward_feat_true(self):
        head = Head()
        input_tensor = torch.randn(1, 3, 64, 64)

        features = head(input_tensor, feat=True)

        self.assertEqual(len(features), 4)
        for feat in features:
            self.assertIsInstance(feat, torch.Tensor)


class TestResConv(TestCase):
    def test_forward_shape(self):
        res_conv = ResConv(n_channels=16)
        input_tensor = torch.randn(1, 16, 32, 32)

        output = res_conv(input_tensor)

        # Aseguramos que la salida tiene el mismo tamaño que la entrada
        self.assertEqual(output.shape, input_tensor.shape)


class TestIFBlock(TestCase):
    def test_forward_no_flow(self):
        block = IFBlock(in_channels=7+8)
        input_tensor = torch.randn(1, 15, 64, 64)  # (batch, channels, height, width)

        flow, mask, feat = block(input_tensor)

        self.assertEqual(flow.shape[1], 4)
        self.assertEqual(mask.shape[1], 1)
        self.assertIsInstance(feat, torch.Tensor)

    def test_forward_with_flow(self):
        block = IFBlock(in_channels=36)
        input_tensor = torch.randn(1, 32, 64, 64)
        flow_tensor = torch.randn(1, 4, 64, 64)

        flow, mask, feat = block(input_tensor, flow_tensor)

        self.assertEqual(flow.shape[1], 4)
        self.assertEqual(mask.shape[1], 1)
        self.assertIsInstance(feat, torch.Tensor)


class TestIFNet(TestCase):
    def setUp(self):
        self._device = torch.device("cpu")
        self._net = IFNet(device=self._device)

    def test_forward(self):
        input_tensor = torch.randn(1, 6, 64, 64)

        scale_list = (8, 4, 2, 1, 1)

        flow_list, mask, merged = self._net(
            input_tensor, scale_list=scale_list
        )

        self.assertEqual(len(flow_list), 5)
        self.assertIsInstance(mask, torch.Tensor)
        self.assertIsInstance(merged, list)
        self.assertIsInstance(merged[-1], torch.Tensor)

    def test_forward_initial_step(self):
        input_tensor = torch.randn(1, 6, 64, 64)
        flow_list, mask, merged = self._net(input_tensor, scale_list=(8, 4, 2, 1, 1))

        self.assertEqual(len(flow_list), 5)
        self.assertEqual(mask.shape, (1, 1, 64, 64))
        self.assertEqual(merged[-1].shape, (1, 3, 64, 64))

    def test_forward_ensemble_mode_warning(self):
        input_tensor = torch.randn(1, 6, 64, 64)
        captured_output = StringIO()
        sys.stdout = captured_output

        self._net(input_tensor, scale_list=(8, 4, 2, 1, 1), ensemble=True)
        sys.stdout = sys.__stdout__

        self.assertIn("warning: ensemble is not supported", captured_output.getvalue())

    def test_forward_merged_final_tensor(self):
        input_tensor = torch.randn(1, 6, 64, 64)

        _, _, merged = self._net(input_tensor, scale_list=(8, 4, 2, 1, 1))

        self.assertIsInstance(merged[4], torch.Tensor)
        self.assertEqual(merged[4].shape, (1, 3, 64, 64))

    def test_forward_timestep_float(self):
        input_tensor = torch.randn(1, 6, 64, 64)
        timestep = 0.7  # float

        flow_list, mask, _ = self._net(input_tensor, timestep=timestep, scale_list=(8, 4, 2, 1, 1))

        self.assertEqual(len(flow_list), 5)
        self.assertEqual(mask.shape, (1, 1, 64, 64))

    def test_forward_timestep_tensor(self):
        input_tensor = torch.randn(1, 6, 64, 64)
        timestep = torch.tensor([0.3])

        flow_list, mask, _ = self._net(input_tensor, timestep=timestep, scale_list=(8, 4, 2, 1, 1))

        self.assertEqual(len(flow_list), 5)
        self.assertEqual(mask.shape, (1, 1, 64, 64))
