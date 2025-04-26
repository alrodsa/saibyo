from libs.base.conf.app import configure
from src.conf.conf import SaibyoConf
from src.constants.app import APP_NAME, ROOT_DIR
from src.core.interpolator import Interpolator


def interpolate(input_folder: str, output_folder: str) -> None:
    conf = configure(APP_NAME, ROOT_DIR, SaibyoConf)

    Interpolator(conf).run(
        input_folder=input_folder,
        output_folder=output_folder,
    )

