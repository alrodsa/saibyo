from pathlib import Path

import torch
from PIL import Image

from src.constants.dataset import IMAGE_EXTENSION


def random_image(width: int = 64, height: int = 64) -> Image.Image:
    """
    Generate a random image with the given width and height.

    Parameters
    ----------
    width : int
        The width of the image.
    height : int
        The height of the image.

    Returns
    -------
    Image.Image
        A random image with the given width and height.

    """
    return Image.fromarray(
        (
            torch.randn(3, width, height) * 255
        ).byte().permute(1, 2, 0).numpy()
    )

def random_images(
    num_frames: int = 4,
    width: int = 64,
    height: int = 64
) -> list[Image.Image]:
    """
    Create a set of images with the given number of frames, width and height.

    Parameters
    ----------
    num_frames : int
        The number of frames to create.
    width : int
        The width of the frames.
    height : int
        The height of the frames.

    Returns
    -------
    list[Image.Image]
        A list of images with the given number of frames, width and height.

    """
    return [random_image(width=width, height=height) for _ in range(num_frames)]

def save_random_images(
    save_dir: str,
    n_images: int = 4,
    width: int = 64,
    height: int = 64,
) -> None:
    """
    Save a set of random images to the given output directory.

    Parameters
    ----------
    save_dir : str
        The output directory to save the images.
    n_images : int
        The number of images to create.
    width : int
        The width of the image.
    height : int
        The height of the image.

    """
    Path(save_dir).mkdir(parents=True, exist_ok=True)

    for i, image in enumerate(random_images(n_images, width, height)):
        image.save(Path(save_dir) / f"image_{i}.{IMAGE_EXTENSION}")
