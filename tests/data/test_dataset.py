import os
import tempfile
from pathlib import Path
from unittest import TestCase

import torch

from src.constants.dataset import IMAGE_EXTENSION
from tests.factories.images import save_random_images


class TestFramePairDataset(TestCase):
    def setUp(self) -> None:
        """
        Set up the test case.
        """
        self._tmp_dir = tempfile.TemporaryDirectory()
        self._input_dir = os.path.join(self._tmp_dir.name, "inputs")
        self._output_dir = os.path.join(self._tmp_dir.name, "outputs")
        Path(self._input_dir).mkdir(parents=True, exist_ok=True)
        Path(self._output_dir).mkdir(parents=True, exist_ok=True)

        # Create random images for testing
        save_random_images(
            save_dir=self._input_dir,
            num_frames=4,
            width=64,
            height=64
        )

    def tearDown(self) -> None:
        """
        Clean up the test case.
        """
        self._tmp_dir.cleanup()

    def test_files(self):
        """
        Test the _files method.
        """
        from src.data.dataset import FramePairDataset

        dataset = FramePairDataset(input_folder=self._input_dir)
        files = dataset._files
        self.assertEqual(len(files), 4)
        self.assertTrue(all(file.endswith(f".{IMAGE_EXTENSION}") for file in files))

    def test_pairs(self):
        """
        Test the _pairs method.
        """
        from src.data.dataset import FramePairDataset

        dataset = FramePairDataset(input_folder=self._input_dir)
        pairs = dataset._pairs
        self.assertEqual(len(pairs), 3)
        self.assertTrue(all(isinstance(pair, tuple) and len(pair) == 2 for pair in pairs))
        self.assertTrue(all(os.path.exists(pair[0]) and os.path.exists(pair[1]) for pair in pairs))

    def test_to_tensor(self):
        """
        Test the _to_tensor method.
        """
        from src.data.dataset import FramePairDataset

        dataset = FramePairDataset(input_folder=self._input_dir)
        tensor = dataset._to_tensor(dataset._files[0])
        self.assertEqual(tensor.shape, (3, 64, 64))
        self.assertTrue(tensor.dtype == torch.float32)

    def test_len(self):
        """
        Test the __len__ method.
        """
        from src.data.dataset import FramePairDataset

        dataset = FramePairDataset(input_folder=self._input_dir)
        self.assertEqual(len(dataset), 3)

    def test_getitem(self):
        """
        Test the __getitem__ method.
        """
        from src.data.dataset import FramePairDataset

        dataset = FramePairDataset(input_folder=self._input_dir)
        item = dataset[0]
        self.assertEqual(len(item), 2)
        self.assertTrue(all(isinstance(path, str) for path in item["paths"]))
        self.assertTrue(all(isinstance(image, torch.Tensor) for image in item["images"]))
        self.assertEqual(item["images"][0].shape, (3, 64, 64))
        self.assertEqual(item["images"][1].shape, (3, 64, 64))
