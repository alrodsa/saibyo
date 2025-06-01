import logging
from functools import cached_property
from pathlib import Path

import cv2
import numpy as np
import torch
from attrs import define, field
from torch.utils.data import DataLoader
from tqdm import tqdm

from saibyo.conf.conf import SaibyoConf
from saibyo.constants.app import APP_NAME, WEIGHTS_DIR
from saibyo.data.dataset import FramePairDataset
from saibyo.model.rife import RifeModel
from saibyo.utils.image import pad_to_multiple


@define
class Interpolator:
    """
    Class to interpolate frames using the RIFE model.
    The class is initialized with a configuration object and the device
    to use for inference. The class loads the interpolation model and provides
    a method to run the interpolation on a given input folder containing
    original frames and save the interpolated frames to a given output folder.

    Parameters
    ----------
    _conf : SaibyoConf
        The configuration object containing the settings for the interpolator.
    _logger : logging.Logger
        The logger object to log messages.
    _model : RifeModel
        The RIFE model object used for interpolation.
    _device : torch.device
        The device to use for inference (CPU or GPU).

    Properties
    ----------
    _n_middle_frames : int
        The number of middle frames to interpolate between two original frames.
        This is calculated as 2 raised to the power of the `exp` attribute
        in the configuration object.

    """

    _conf: SaibyoConf

    _logger: logging.Logger = field(factory=lambda: logging.getLogger(APP_NAME))
    _model: RifeModel = field(default=None, init=False)
    _device: torch.device = field(default=torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"), init=True
    )

    @cached_property
    def _n_middle_frames(self) -> int:
        """
        Get the number of middle frames to interpolate.

        Returns
        -------
        int
            The number of middle frames to interpolate.

        """
        return 2 ** self._conf.interpolator.exp

    def __attrs_post_init__(self) -> None:
        """
        Initialize the interpolator, set the device and load the model.
        """
        self._model = RifeModel(self._device)
        self._model.load(path=WEIGHTS_DIR)
        self._logger.debug("[✅] Model loaded successfully.")
        self._info()

    def _info(self) -> None:
        """
        Print the information about the interpolator.
        """
        self._logger.info(f"[🚀] Device: {self._device}")
        self._logger.info(f"[📦] Batch size: {self._conf.interpolator.batch_size}")
        self._logger.info(f"[💼] Num workers: {self._conf.interpolator.num_workers}")
        self._logger.info(f"[⚙️] Number of middle frames: {self._n_middle_frames}")

    def _interpolate(self, dataloader: DataLoader, output_folder: str) -> None:
        """
        Interpolate the frames in the dataloader and save them to the output folder.

        Parameters
        ----------
        dataloader : DataLoader
            The dataloader containing the frames to interpolate.
        output_folder : str
            The path to the output folder where the interpolated frames will be saved.

        """
        self._model.eval()

        with torch.no_grad():
            actual_frame = 0
            for batch_idx, batch in tqdm(
                enumerate(dataloader), total=len(dataloader), desc="Batches"
            ):
                for _, item in tqdm(
                    enumerate(batch),
                    total=len(batch),
                    desc=f"Items in batch {batch_idx}", leave=False
                ):
                    img_list = []

                    image_1 = item["images"][0].to(self._device)
                    image_2 = item["images"][1].to(self._device)

                    if batch_idx == 0:
                        img_list.append(
                            image_1.cpu().numpy().transpose(1, 2, 0) * 255
                        )  # [H, W, 3]

                    img1_padded, h, w = pad_to_multiple(image_1) # [3, H, W]
                    img2_padded, _, _ = pad_to_multiple(image_2) # [3, H, W]

                    img1_padded = img1_padded.unsqueeze(0)  # [1, 3, H, W]
                    img2_padded = img2_padded.unsqueeze(0)  # [1, 3, H, W]

                    interpolated_frames = []
                    for n in range(self._n_middle_frames-1):
                        interpolated_frame = self._model.inference(
                            img1_padded, img2_padded, (n+1) * 1. / self._n_middle_frames
                        )
                        interpolated_frames.append(interpolated_frame)

                    # Post-process the interpolated frames
                    for n in range(len(interpolated_frames)):
                        img = interpolated_frames[n][0]  # [3, H, W]
                        img = img.cpu().numpy().transpose(1, 2, 0)  # [H, W, 3]
                        img = (img * 255).astype(np.uint8)
                        img = img[:h, :w]  # recortamos padding
                        img_list.append(img)

                    img_list.append(
                        image_2.clamp(0, 1).cpu().numpy().transpose(
                            1, 2, 0
                        ) * 255
                    )  # [H, W, 3]

                    # Save the images (original and interpolated) to output folder
                    for _, img in enumerate(img_list):
                        out_path = Path(output_folder) / f"frame_{actual_frame:06}.png"
                        cv2.imwrite(out_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
                        actual_frame += 1

    def run(self, input_folder: str, output_folder: str) -> "Interpolator":
        """
        Run the interpolator.

        Parameters
        ----------
        input_folder : str
            The path to the input folder where the original frames are stored.
        output_folder : str
            The path to the output folder where both the original and
            interpolated frames will be stored.

        """
        self._logger.info(f"[📂] Input folder: {input_folder}")

        # Create Dataset
        dataset = FramePairDataset(input_folder=input_folder)

        # Create Dataloader
        dataloader =  DataLoader(
            dataset,
            batch_size=self._conf.interpolator.batch_size,
            num_workers=self._conf.interpolator.num_workers,
            shuffle=False,
            collate_fn=lambda x: x,
        )

        # Create output folder if it doesn't exist
        Path(output_folder).mkdir(parents=True, exist_ok=True)
        self._logger.info(f"[📂] Output folder: {output_folder}")

        # Interpolate
        self._interpolate(dataloader=dataloader, output_folder=output_folder)

        return self

