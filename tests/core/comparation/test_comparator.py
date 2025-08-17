from unittest import TestCase
from unittest.mock import call, patch

import numpy as np

from saibyo.conf.conf import SaibyoConf
from saibyo.core.comparation.comparator import Comparator
from saibyo.metadata.video import VideoMetadata


class TestComparator(TestCase):
    @patch.dict(
        "os.environ",
        {
            "SAIBYO_INTERPOLATOR_COMPARATION": "False",
            "SAIBYO_INTERPOLATOR_LIGHTWEIGHT": "True",
            "SAIBYO_INTERPOLATOR_EXPONENTIAL": "3",
            "SAIBYO_COMPARATOR_OVERLAY_TEXT_OVERLAY": "True",
            "SAIBYO_COMPARATOR_OVERLAY_TEXT_POSITION": "top_left",
            "SAIBYO_COMPARATOR_BACKGROUND_COLOR": "#000000",
            "SAIBYO_COMPARATOR_MODE": "side_by_side"
        }
    )
    def setUp(self):
        self.conf = SaibyoConf()

    @patch("saibyo.core.comparation.comparator.VideoMetadata", spec=VideoMetadata)
    @patch("saibyo.core.comparation.comparator.ComparationEngine")
    def test_compare(self, mock_comparation_engine, mock_video_metadata):
        video_a = "path/to/video_a.mp4"
        video_b = "path/to/video_b.mp4"
        output_path = "path/to/output.mp4"

        mock_engine_instance = mock_comparation_engine.return_value
        fake_result = np.zeros((2, 2), dtype=np.uint8)
        mock_engine_instance.compare.return_value = fake_result

        comparator = Comparator(self.conf.comparator)

        result = comparator.compare(video_a, video_b, output_path)

        mock_comparation_engine.assert_called_once_with(self.conf.comparator)
        mock_engine_instance.compare.assert_called_once()
        kwargs = mock_engine_instance.compare.call_args.kwargs
        self.assertIs(kwargs["video_a"], mock_video_metadata.return_value)
        self.assertIs(kwargs["video_b"], mock_video_metadata.return_value)
        self.assertEqual(kwargs["output_path"], output_path)
        self.assertEqual(
            mock_video_metadata.call_args_list,
            [
                call(input_path=video_a),
                call(input_path=video_b),
                call(input_path=video_a),
                call(input_path=video_b),
            ],
        )

        self.assertTrue(np.array_equal(result, fake_result))
