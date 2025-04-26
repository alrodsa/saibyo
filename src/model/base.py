from abc import ABC, abstractmethod

import torch


class BaseInterpolationModel(ABC):
    """
    Base class for all interpolation models.
    """

    @abstractmethod
    def load(self, path: str) -> "BaseInterpolationModel":
        """
        Load the model weights from the specified path.

        Parameters
        ----------
        path : str
            The path to the model weights file.

        Returns
        -------
        BaseInterpolationModel
            The current instance of the BaseInterpolationModel class.

        """
        ...

    @abstractmethod
    def inference(self) -> torch.Tensor:
        """
        Perform inference on the input images.

        Returns
        -------
        torch.Tensor
            The interpolated image.

        """
        ...
