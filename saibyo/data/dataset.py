from functools import cached_property
from pathlib import Path

import cv2
import torch
from attrs import define, field
from torch.utils.data import Dataset
from torchvision import transforms

from saibyo.constants.dataset import IMAGE_EXTENSION


@define
class FramePairDataset(Dataset):
    """
    Dataset class for loading pairs of images from a folder.
    This class is used to load pairs of images from a folder and return them
    as a dictionary containing the images and their paths. The images are
    transformed to tensors using the specified transform.

    Attributes
    ----------
    input_folder : str
        The folder containing the images.
    transform : transforms.Compose
        The transform to apply to the images.

    """

    input_folder: str
    transform: transforms.Compose = field(
        default=transforms.Compose([transforms.ToTensor()])
    )

    @cached_property
    def _files(self) -> list[str]:
        return sorted(
            [
                str(p)
                for p in Path(self.input_folder).glob(f"*.{IMAGE_EXTENSION}")
            ]
        )

    @cached_property
    def _pairs(self) -> list[tuple[str, str]]:
        return [
            (self._files[i], self._files[i+1])
            for i in range(len(self._files)-1)
        ]

    def _to_tensor(self, image_path: str) -> torch.tensor:
        """
        Converts an image to a tensor.

        Parameters
        ----------
        image_path : str
            The path to the image.

        Returns
        -------
        torch.tensor
            The image as a tensor.

        """
        return self.transform(
            cv2.cvtColor(
                cv2.imread(image_path, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB
            )
        )

    def __len__(self) -> int:
        """
        Returns the number of pairs of images in the dataset.
        """
        return len(self._pairs)

    def __getitem__(self, idx: int) -> dict:
        """
        Returns a pair of images and their paths.

        Parameters
        ----------
        idx : int
            The index of the pair of images to return.

        Returns
        -------
        dict
            A dictionary containing the pair of images and their paths.
            The dictionary has the following keys:
            - "images": A tuple of two images.
            - "paths": A tuple of two paths.

        """
        path1, path2 = self._pairs[idx]
        img1 = self._to_tensor(path1)
        img2 = self._to_tensor(path2)

        return {"images": (img1, img2), "paths": (path1, path2)}
