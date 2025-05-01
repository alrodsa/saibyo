from unittest import TestCase
from unittest.mock import patch

from saibyo.conf.conf import InterpolatorConf, SaibyoConf


class TestInterpolatorConf(TestCase):
    @patch.dict("os.environ", {
        "SAIBYO_INTERPOLATOR_BATCH_SIZE": "8",
        "SAIBYO_INTERPOLATOR_NUM_WORKERS": "2",
        "SAIBYO_INTERPOLATOR_EXP": "3"
    })
    def test_interpolator_conf(self):
        conf = InterpolatorConf()

        self.assertEqual(conf.batch_size, 8)
        self.assertEqual(conf.num_workers, 2)
        self.assertEqual(conf.exp, 3)

class TestSaibyoConf(TestCase):
    @patch.dict("os.environ", {
        "SAIBYO_INTERPOLATOR_BATCH_SIZE": "1",
        "SAIBYO_INTERPOLATOR_NUM_WORKERS": "0",
        "SAIBYO_INTERPOLATOR_EXP": "1"
    })
    def test_saibyo_conf(self):
        conf = SaibyoConf(
            interpolator=InterpolatorConf()
        )

        self.assertEqual(conf.interpolator.batch_size, 1)
        self.assertEqual(conf.interpolator.num_workers, 0)
        self.assertEqual(conf.interpolator.exp, 1)
