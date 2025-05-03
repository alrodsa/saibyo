import tempfile
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock

from saibyo.model.rife import RifeModel
from tests.factories.images import save_random_images


class TestInterpolator(TestCase):
    def setUp(self) -> None:
        """
        Set up the test case.
        """
        self._conf = MagicMock(
            interpolator=MagicMock(
                exp=2,
                batch_size=4,
                num_workers=0
            )
        )
        self._device = "cpu"
        self._model = RifeModel(device=self._device)
        self._tmp_dir = tempfile.TemporaryDirectory()
        self._input_dir = Path(self._tmp_dir.name) / "inputs"
        self._output_dir = Path(self._tmp_dir.name) / "outputs"

        # Create random images for testing
        save_random_images(
            save_dir=self._input_dir,
            n_images=4,
            width=64,
            height=64
        )

    def tearDown(self) -> None:
        """
        Clean up the test case.
        """
        self._tmp_dir.cleanup()

    def test_interpolate(self):
        """
        Test the interpolate method.
        """
        pass



