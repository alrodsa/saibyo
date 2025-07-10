from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from saibyo.base.conf.schema import Conf
from saibyo.constants.conf import (
    COMPARATION_DESCRIPTION,
    EXPONENTIAL_DESCRIPTION,
    LIGHTWEIGHT_DESCRIPTION,
)


class InterpolatorConf(BaseSettings):
    """
    Configuration for the Interpolator.

    Attributes
    ----------
    comparation : bool
        If True, creates an extra video that compares the original video with the
        interpolated video, showing the differences between them.
    lightweight : bool
        If True, the model inference will be performed using fp16 precision,
        which is faster and uses less memory, but may result in lower quality output.
    exponential : int
        The value of the exponential parameter is used to determine the value of the
        fps multiplier, which is calculated as 2 ** exponential. For example:
        - If exponential is 1, the fps multiplier is 2 ** 1 = 2, resulting in
        double the frames.
        - If exponential is 2, the fps multiplier is 2 ** 2 = 4, resulting in
        quadruple the frames.
        - If exponential is 3, the fps multiplier is 2 ** 3 = 8, resulting in
        eight times the frames.
        This allows for flexible control over the frame rate increase during
        interpolation.

    """

    comparation: bool = Field(default=False, description=COMPARATION_DESCRIPTION)
    lightweight: bool = Field(default=True, description=LIGHTWEIGHT_DESCRIPTION)
    exponential: int = Field(default=2, description=EXPONENTIAL_DESCRIPTION)

    model_config = SettingsConfigDict(env_prefix="SAIBYO_INTERPOLATOR_")

class SaibyoConf(Conf, BaseSettings):
    """
    Configuration for the Saibyo application.

    Attributes
    ----------
    interpolator : InterpolatorConf
        Configuration for the interpolator.

    """

    interpolator: InterpolatorConf= Field(default_factory=InterpolatorConf)

    model_config = SettingsConfigDict(env_prefix="SAIBYO_")



