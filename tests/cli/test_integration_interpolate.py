import tempfile
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from src.conf.conf import InterpolatorConf, SaibyoConf
from src.constants.dataset import IMAGE_EXTENSION
from tests.factories.images import save_random_images


class TestInterpolateCLI(TestCase):
    def setUp(self) -> None:
        """
        Set up the test case.
        """
        self._tmp_dir = tempfile.TemporaryDirectory()
        self._input_dir = Path(self._tmp_dir.name) / "inputs"
        self._output_dir = Path(self._tmp_dir.name) / "outputs"

        self._conf = SaibyoConf(
            interpolator=InterpolatorConf(
                batch_size=1,
                num_workers=0,
                exp=1,
            )
        )

        self._input_dir.mkdir(parents=True, exist_ok=True)
        self._output_dir.mkdir(parents=True, exist_ok=True)

        save_random_images(
            save_dir=str(self._input_dir),
            n_images=2,
            width=128,
            height=128,
        )

    def tearDown(self) -> None:
        """
        Clean up the test case.
        """
        self._tmp_dir.cleanup()

    @patch("src.cli.interpolate.configure")
    def test_interpolate(self, mock_configure):
        """
        Test the interpolate function.
        """
        mock_configure.return_value = self._conf
        from src.cli.interpolate import interpolate

        interpolation = interpolate(
            input_folder=str(self._input_dir),
            output_folder=str(self._output_dir),
        )

        # Check that the output folder contains the expected number of files
        output_files = list(self._output_dir.glob(f"*.{IMAGE_EXTENSION}"))
        self.assertEqual(len(output_files), 2 * (2 ** self._conf.interpolator.exp) - 1)

        # Check that the output files are not empty
        for output_file in output_files:
            self.assertTrue(output_file.stat().st_size > 0)

        # Check that the output files are in the expected format
        for output_file in output_files:
            self.assertTrue(output_file.suffix == f".{IMAGE_EXTENSION}")

        # Check that the interpolate function returns the expected type
        self.assertTrue(interpolation is None)
