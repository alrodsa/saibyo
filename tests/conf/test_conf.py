from unittest import TestCase
from unittest.mock import patch

from saibyo.conf.conf import SaibyoConf

SAIBYO_INTERPOLATOR_COMPARATION = "False"
SAIBYO_INTERPOLATOR_LIGHTWEIGHT = "False"
SAIBYO_INTERPOLATOR_EXPONENTIAL = "10"
SAIBYO_COMPARATOR_OVERLAY_TEXT_OVERLAY = "False"
SAIBYO_COMPARATOR_OVERLAY_TEXT_POSITION = "bottom_right"
SAIBYO_COMPARATOR_BACKGROUND_COLOR = "#FFFFFF"
SAIBYO_COMPARATOR_MODE = "top_bottom"


class TestSaibyoConf(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    @patch.dict(
        "os.environ",
        {
            "SAIBYO_INTERPOLATOR_COMPARATION": SAIBYO_INTERPOLATOR_COMPARATION,
            "SAIBYO_INTERPOLATOR_LIGHTWEIGHT": SAIBYO_INTERPOLATOR_LIGHTWEIGHT,
            "SAIBYO_INTERPOLATOR_EXPONENTIAL": SAIBYO_INTERPOLATOR_EXPONENTIAL,
            "SAIBYO_COMPARATOR_OVERLAY_TEXT_OVERLAY": SAIBYO_COMPARATOR_OVERLAY_TEXT_OVERLAY,
            "SAIBYO_COMPARATOR_OVERLAY_TEXT_POSITION": SAIBYO_COMPARATOR_OVERLAY_TEXT_POSITION,
            "SAIBYO_COMPARATOR_BACKGROUND_COLOR": SAIBYO_COMPARATOR_BACKGROUND_COLOR,
            "SAIBYO_COMPARATOR_MODE": SAIBYO_COMPARATOR_MODE
        }
    )
    def test_saibyo_conf(self):

        saibyo_conf =  SaibyoConf()

        self.assertFalse(saibyo_conf.interpolator.comparation)
        self.assertFalse(saibyo_conf.interpolator.lightweight)
        self.assertEqual(saibyo_conf.interpolator.exponential, int(SAIBYO_INTERPOLATOR_EXPONENTIAL))
        self.assertFalse(saibyo_conf.comparator.text.overlay)
        self.assertEqual(saibyo_conf.comparator.text.position, SAIBYO_COMPARATOR_OVERLAY_TEXT_POSITION)
        self.assertEqual(saibyo_conf.comparator.background_color, SAIBYO_COMPARATOR_BACKGROUND_COLOR)
        self.assertEqual(saibyo_conf.comparator.mode, SAIBYO_COMPARATOR_MODE)

class TestInterpolatorConf(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    @patch.dict(
        "os.environ",
        {
            "SAIBYO_INTERPOLATOR_COMPARATION": SAIBYO_INTERPOLATOR_COMPARATION,
            "SAIBYO_INTERPOLATOR_LIGHTWEIGHT": SAIBYO_INTERPOLATOR_LIGHTWEIGHT,
            "SAIBYO_INTERPOLATOR_EXPONENTIAL": SAIBYO_INTERPOLATOR_EXPONENTIAL
        }
    )
    def test_interpolator_conf(self):
        from saibyo.conf.conf import InterpolatorConf

        interpolator_conf = InterpolatorConf()

        self.assertFalse(interpolator_conf.comparation)
        self.assertFalse(interpolator_conf.lightweight)
        self.assertEqual(interpolator_conf.exponential, int(SAIBYO_INTERPOLATOR_EXPONENTIAL))


class TestComparatorConf(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    @patch.dict(
        "os.environ",
        {
            "SAIBYO_COMPARATOR_OVERLAY_TEXT_OVERLAY": SAIBYO_COMPARATOR_OVERLAY_TEXT_OVERLAY,
            "SAIBYO_COMPARATOR_OVERLAY_TEXT_POSITION": SAIBYO_COMPARATOR_OVERLAY_TEXT_POSITION,
            "SAIBYO_COMPARATOR_BACKGROUND_COLOR": SAIBYO_COMPARATOR_BACKGROUND_COLOR,
            "SAIBYO_COMPARATOR_MODE": SAIBYO_COMPARATOR_MODE
        }
    )
    def test_comparator_conf(self):
        from saibyo.conf.conf import ComparatorConf

        comparator_conf = ComparatorConf()

        self.assertFalse(comparator_conf.text.overlay)
        self.assertEqual(comparator_conf.text.position, SAIBYO_COMPARATOR_OVERLAY_TEXT_POSITION)
        self.assertEqual(comparator_conf.background_color, SAIBYO_COMPARATOR_BACKGROUND_COLOR)
        self.assertEqual(comparator_conf.mode, SAIBYO_COMPARATOR_MODE)
