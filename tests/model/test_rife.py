from unittest import TestCase
from unittest.mock import MagicMock, patch

import torch

from saibyo.model.rife import RifeModel
from saibyo.modules.ifnet import IFNet


class TestRifeModel(TestCase):
    def setUp(self) -> None:
        """
        Set up the test case by initializing the RifeModel instance.
        """
        self._device = (
            torch.device("cuda")
            if torch.cuda.is_available() else torch.device("cpu")
        )
        self._weight_path = "path/to/model/weights.pth"

    @patch("saibyo.model.rife.torch.load")
    def test_load(self, mock_load):
        mock_state_dict = {
            "module.conv1.weight": MagicMock(),
            "module.conv1.bias": MagicMock()
        }
        mock_load.return_value = mock_state_dict

        model = RifeModel(self._device)
        returned_model = model.load(self._weight_path)

        self.assertEqual(returned_model, model)

    def test_eval(self):
        model = RifeModel(self._device)
        model._flownet = MagicMock()
        model.eval()

        model._flownet.eval.assert_called_once()

    def test_inference(self):
        model = RifeModel(device=torch.device("cpu"))

        mock_merged = [torch.rand(1, 3, 64, 64)]
        model._flownet = MagicMock(return_value=(None, None, mock_merged))

        img0 = torch.rand(1, 3, 64, 64)
        img1 = torch.rand(1, 3, 64, 64)

        output = model.inference(img0, img1)

        model._flownet.assert_called_once()
        self.assertTrue(torch.equal(output, mock_merged[-1]))
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0].shape, (3, 64, 64))
