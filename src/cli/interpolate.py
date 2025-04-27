from libs.base.conf.app import configure
from src.conf.conf import SaibyoConf
from src.constants.app import APP_NAME, ROOT_DIR
from src.core.interpolator import Interpolator


def interpolate(input_folder: str, output_folder: str) -> None:
    """
    Interpolates the data in the input folder and saves it to the output folder.

    Parameters
    ----------
    input_folder : str
        The path to the input folder containing the data to be interpolated.
    output_folder : str
        The path to the output folder where the interpolated data will be saved.

    """
    conf = configure(APP_NAME, ROOT_DIR, SaibyoConf)

    Interpolator(conf).run(
        input_folder=input_folder,
        output_folder=output_folder,
    )

