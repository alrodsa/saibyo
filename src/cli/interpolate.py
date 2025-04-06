import logging

from libs.base.conf.app import configure
from src.constants.app import APP_NAME, ROOT_DIR


def interpolate() -> None:

    conf = configure(APP_NAME, ROOT_DIR, None)
    logger = logging.getLogger(APP_NAME)

