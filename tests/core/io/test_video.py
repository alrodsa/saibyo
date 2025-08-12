import threading
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import numpy as np

from saibyo.core.io.video import VideoIOManager


class TestVideoIOManager(unittest.TestCase):
    def setUp(self) -> None:
        # Stub sencillo de VideoMetadata
        self.video_meta = SimpleNamespace(
            width=1920,
            height=1080,
            input_path="/videos/input.mp4",
        )
        self.fps = 97.4
        self.output_path = "/out/out.mp4"

    @patch("saibyo.core.io.video._thread.start_new_thread")
    @patch("saibyo.core.io.video.cv2.VideoWriter_fourcc")
    @patch("saibyo.core.io.video.cv2.VideoWriter")
    def test_init_sets_up_writer_queues_and_starts_threads(
        self, mock_video_writer, mock_fourcc, mock_start_new_thread
    ):
        mock_fourcc.return_value = 1234

        # Crear instancia (esto llama _start_threads con el path)
        mgr = VideoIOManager(video=self.video_meta, fps=self.fps, output_path=self.output_path)

        # VideoWriter se crea con round(fps) y tamaño (width, height)
        mock_fourcc.assert_called_once_with(*"mp4v")
        mock_video_writer.assert_called_once()
        args, kwargs = mock_video_writer.call_args
        self.assertEqual(args[0], self.output_path)
        self.assertEqual(args[1], mock_fourcc.return_value)
        self.assertEqual(args[2], round(self.fps))
        self.assertEqual(args[3], (self.video_meta.width, self.video_meta.height))

        # Existen colas con capacidad 500
        self.assertEqual(mgr.write_buffer.maxsize, 500)
        self.assertEqual(mgr.read_buffer.maxsize, 500)

        # Se arrancan 2 hilos: lector y escritor
        self.assertEqual(mock_start_new_thread.call_count, 2)

        # Primer hilo: _build_read_buffer(video_path)
        first_call_args = mock_start_new_thread.call_args_list[0].args
        target1, args1 = first_call_args
        # Verifica que el target es el método correcto sobre la instancia correcta
        self.assertIs(target1.__func__, VideoIOManager._build_read_buffer)
        self.assertIs(target1.__self__, mgr)
        self.assertEqual(args1, (self.video_meta.input_path,))

        # Segundo hilo: _clear_write_buffer()
        second_call_args = mock_start_new_thread.call_args_list[1].args
        target2, args2 = second_call_args
        self.assertIs(target2.__func__, VideoIOManager._clear_write_buffer)
        self.assertIs(target2.__self__, mgr)
        self.assertEqual(args2, ())

    @patch("saibyo.core.io.video.cv2.VideoCapture")
    @patch("saibyo.core.io.video.cv2.cvtColor")
    def test_build_read_buffer_reads_frames_and_sends_none(self, mock_cvt_color, mock_video_capture):
        # Evitar que __init__ lance hilos: parcheamos _start_threads durante la construcción
        with patch.object(VideoIOManager, "_start_threads", lambda *a, **k: None):
            mgr = VideoIOManager(video=self.video_meta, fps=self.fps, output_path=self.output_path)

        # Simular VideoCapture con dos frames y luego EOF
        bgr1 = np.zeros((2, 2, 3), dtype=np.uint8)
        bgr2 = np.ones((2, 2, 3), dtype=np.uint8) * 255
        rgb1 = np.full((2, 2, 3), 10, dtype=np.uint8)
        rgb2 = np.full((2, 2, 3), 20, dtype=np.uint8)

        cap_instance = mock_video_capture.return_value
        cap_instance.read.side_effect = [
            (True, bgr1),
            (True, bgr2),
            (False, None),
        ]
        mock_cvt_color.side_effect = [rgb1, rgb2]

        # Ejecutar el método directamente (sin hilo)
        mgr._build_read_buffer(self.video_meta.input_path)

        # Leímos 2 frames y un None al final
        frame_a = mgr.read_buffer.get_nowait()
        frame_b = mgr.read_buffer.get_nowait()
        end_marker = mgr.read_buffer.get_nowait()

        self.assertTrue(np.array_equal(frame_a, rgb1))
        self.assertTrue(np.array_equal(frame_b, rgb2))
        self.assertIsNone(end_marker)

        cap_instance.release.assert_called_once()

    @patch("saibyo.core.io.video.cv2.VideoWriter")
    def test_clear_write_buffer_writes_until_none_and_bgr_flip(self, mock_video_writer):
        # Evitar hilos en __init__
        with patch.object(VideoIOManager, "_start_threads", lambda *a, **k: None):
            mgr = VideoIOManager(video=self.video_meta, fps=self.fps, output_path=self.output_path)

        # Preparar frames RGB y lo que se debería escribir (BGR)
        rgb_a = np.random.randint(0, 255, (3, 3, 3), dtype=np.uint8)
        rgb_b = np.random.randint(0, 255, (3, 3, 3), dtype=np.uint8)
        expected_a = rgb_a[:, :, ::-1]
        expected_b = rgb_b[:, :, ::-1]

        writer = mock_video_writer.return_value
        writer.write = MagicMock()

        # Encolar frames y el terminador
        mgr.write_buffer.put(rgb_a)
        mgr.write_buffer.put(rgb_b)
        mgr.write_buffer.put(None)

        # Ejecutar método (sin hilo)
        mgr._clear_write_buffer()

        # writer.write llamado con los frames convertidos a BGR
        self.assertEqual(writer.write.call_count, 2)
        got_a = writer.write.call_args_list[0][0][0]
        got_b = writer.write.call_args_list[1][0][0]
        self.assertTrue(np.array_equal(got_a, expected_a))
        self.assertTrue(np.array_equal(got_b, expected_b))

    @patch("saibyo.core.io.video.cv2.VideoWriter")
    def test_finish_puts_none_and_releases(self, mock_video_writer):
        # Evitar hilos en __init__
        with patch.object(VideoIOManager, "_start_threads", lambda *a, **k: None):
            mgr = VideoIOManager(video=self.video_meta, fps=self.fps, output_path=self.output_path)

        writer = mock_video_writer.return_value
        writer.release = MagicMock()

        # Consumidor que simula el hilo de escritura y vacía la cola
        def consumer():
            # Consumimos exactamente un elemento (el None que pone finish)
            item = mgr.write_buffer.get()
            # No escribimos nada; simplemente liberamos para que finish detecte cola vacía

        t = threading.Thread(target=consumer)
        t.start()

        # Act
        mgr.finish()

        # Assert: la cola queda vacía y se liberan recursos
        t.join(timeout=2.0)
        self.assertTrue(mgr.write_buffer.empty())
        writer.release.assert_called_once()
