from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from libs.base.conf.schema import Conf


class InterpolatorConf(BaseSettings):
    """
    Configuration for the interpolator.

    Attributes
    ----------
    batch_size : int
        The number of pair of images to process in a batch.
    exp : int
        The number of frames to interpolate. This number is used in the
        following way: `n_frames = 2 ** exp`. For example:
        -  If `exp=1` then: `n_frames = 2 ** 1 = 2` which means 1 interpolated
        frame between the two input frames. FPS will be multiplied by 2.
        -  If `exp=2` then: `n_frames = 2 ** 2 = 4` which means 3 interpolated
        frames between the two input frames. FPS will be multiplied by 4.
        -  If `exp=3` then: `n_frames = 2 ** 3 = 8` which means 7 interpolated
        frames between the two input frames. FPS will be multiplied by 8.

    """

    batch_size: int = Field(default=1, gt=0)
    num_workers: int = Field(default=4, ge=0)
    exp: int = Field(default=1, gt=0)

    model_config = SettingsConfigDict(env_prefix="SAIBYO_INTERPOLATOR_")

class SaibyoConf(Conf, BaseSettings):
    """
    Configuration for the Saibyo application.

    Attributes
    ----------
    interpolator : InterpolatorConf
        Configuration for the interpolator.

    """

    interpolator: InterpolatorConf

    model_config = SettingsConfigDict(env_prefix="SAIBYO_")



