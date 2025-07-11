import logging
from dataclasses import dataclass, field

from saibyo.conf.conf import ComparatorConf
from saibyo.constants.app import APP_NAME
from saibyo.metadata.video import VideoMetadata


@dataclass(frozen=True)
class Comparator:
    _conf: ComparatorConf
    _logger: logging.Logger = field(
        default_factory=lambda: logging.getLogger(APP_NAME)
    )

    def compare(self, video_a: str, video_b: str, output_path: str) -> None:
        """
        Creates a comparison video between two input videos. The comparison is
        created taking into account the configuration settings from the ComparatorConf.

        Parameters
        ----------
        video_a : str
            The path to the first video file to be compared.
        video_b : str
            The path to the second video file to be compared.
        output_path : str
            The path where the comparison video will be saved.

        """
        self._logger.info(f"Comparing {video_a} and {video_b}...")

        video_a = VideoMetadata(input_path=video_a)
        video_b = VideoMetadata(input_path=video_b)
        video_a.info()
        video_b.info()

        

        self._logger.info(f"Comparison video saved to {output_path}.")

