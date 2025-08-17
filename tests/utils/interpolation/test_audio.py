import io
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from saibyo.utils.interpolation.audio import transfer_audio


class TestTransferAudio(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.old_cwd = os.getcwd()
        os.chdir(self.tmp.name)
        self.addCleanup(lambda: os.chdir(self.old_cwd))

        self.source = Path("source.mp4")
        self.target = Path("target.mp4")
        self.source.write_bytes(b"SRC")
        self.target.write_bytes(b"VIDEO")

    def _side_effect_factory(self, lossless_ok: bool, aac_ok: bool):
        def _side_effect(args, check=False, stdout=None, stderr=None):
            out = Path(args[-1])

            # Extracción de audio (mkv/m4a): siempre generamos un archivo
            if out.suffix in {".mkv", ".m4a"}:
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(b"AUDIO")
                return 0

            # Combinar a MP4
            if out.suffix == ".mp4" and "-c" in args and "copy" in args and out.name == "target.mp4":
                out.parent.mkdir(parents=True, exist_ok=True)
                if lossless_ok:
                    out.write_bytes(b"MERGED_LOSSLESS")
                elif aac_ok:
                    out.write_bytes(b"MERGED_AAC")
                else:
                    # Simula fallo de ffmpeg dejando un archivo vacío
                    out.write_bytes(b"")
                return 0

            return 0
        return _side_effect

    @patch("saibyo.utils.interpolation.audio.subprocess.run")
    def test_lossless_success(self, mock_run):
        mock_run.side_effect = self._side_effect_factory(lossless_ok=True, aac_ok=False)

        transfer_audio(self.source, self.target)

        self.assertTrue(self.target.exists())
        self.assertGreater(self.target.stat().st_size, 0)
        self.assertFalse(Path("target_noaudio.mp4").exists())
        self.assertFalse(Path(".tmp").exists())
        self.assertEqual(self.target.read_bytes(), b"MERGED_LOSSLESS")
        # 2 llamadas: extraer mkv + combinar
        self.assertEqual(mock_run.call_count, 2)

    @patch("saibyo.utils.interpolation.audio.subprocess.run")
    def test_fallback_to_aac_when_lossless_fails(self, mock_run):
        mock_run.side_effect = self._side_effect_factory(lossless_ok=False, aac_ok=True)

        transfer_audio(self.source, self.target)

        self.assertTrue(self.target.exists())
        self.assertGreater(self.target.stat().st_size, 0)
        self.assertFalse(Path("target_noaudio.mp4").exists())
        self.assertFalse(Path(".tmp").exists())
        self.assertEqual(self.target.read_bytes(), b"MERGED_AAC")
        self.assertEqual(mock_run.call_count, 2)

    @patch("saibyo.utils.interpolation.audio.subprocess.run")
    def test_both_lossless_and_aac_fail(self, mock_run):
        mock_run.side_effect = self._side_effect_factory(lossless_ok=False, aac_ok=False)

        # guarda contenido inicial del target para comprobar que vuelve al original
        initial = self.target.read_bytes()
        transfer_audio(self.source, self.target)

        self.assertTrue(self.target.exists())
        self.assertGreater(self.target.stat().st_size, 0)
        self.assertFalse(Path("target_noaudio.mp4").exists())
        self.assertFalse(Path(".tmp").exists())
        self.assertEqual(self.target.read_bytes(), initial)
        self.assertEqual(mock_run.call_count, 4)
