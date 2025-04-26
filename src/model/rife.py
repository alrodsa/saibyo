import torch
from attrs import define, field

from src.model.base import BaseInterpolationModel
from src.modules.ifnet import IFNet


@define
class RifeModel(BaseInterpolationModel):
    """
    Model class for the interpolation model.
    This class is responsible for loading the model and performing inference.

    Attributes
    ----------
    device : torch.device
        The device to run the model on (CPU or GPU).
    flownet : IFNet
        The flow network model.

    """

    _device: torch.device

    _flownet: IFNet = field(default=None, init=False)

    def __attrs_post_init__(self) -> None:
        """
        Initialize the model, set the device and puts the model in evaluation mode.
        """
        self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._flownet = IFNet(self._device).to(self._device)

    def load(self, path: str) -> "RifeModel":
        """
        Load the model weights from the specified path.

        Parameters
        ----------
        path : str
            The path to the model weights file.

        Returns
        -------
        InterpolationModel
            The current instance of the InterpolationModel class.

        """
        state_dict = torch.load(path, map_location=self._device)
        state_dict = {k.replace("module.", ""): v for k, v in state_dict.items()}
        self._flownet.load_state_dict(state_dict, strict=False)
        return self

    def eval(self) -> None:
        """
        Set the model to evaluation mode.
        """
        self._flownet.eval()

    def inference(
        self,
        img0: torch.Tensor,
        img1: torch.Tensor,
        timestep: float = 0.5,
        scale: float = 1.0
    ) -> torch.Tensor:
        """
        Perform inference on the input images.

        Parameters
        ----------
        img0 : torch.Tensor
            The first input image.
        img1 : torch.Tensor
            The second input image.
        timestep : float, optional
            The interpolation factor (default is 0.5).
        scale : float, optional
            The scale factor for the input images (default is 1.0).

        Returns
        -------
        torch.Tensor
            The interpolated image.

        """
        img0 = img0.to(self._device)
        img1 = img1.to(self._device)
        imgs = torch.cat((img0, img1), dim=1)
        scale_list = [16/scale, 8/scale, 4/scale, 2/scale, 1/scale]

        _, _, merged = self._flownet(imgs, timestep, scale_list)

        return merged[-1]
