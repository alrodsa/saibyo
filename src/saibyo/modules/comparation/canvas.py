import cv2
import numpy as np

from saibyo.constants.conf import ModeType
from saibyo.metadata.video import VideoMetadata
from saibyo.utils.comparation.color import hex_to_rgb
from saibyo.utils.comparation.frame import put_text


class Canvas:
    @staticmethod
    def dimensions_canvas(
        video_a: VideoMetadata, video_b: VideoMetadata, mode: ModeType
    ) -> tuple[int, int]:
        match mode:
            case "side_by_side":
                width = video_a.width + video_b.width
                height = max(video_a.height, video_b.height)
            case "top_bottom":
                width = max(video_a.width, video_b.width)
                height = video_a.height + video_b.height
            case "split_half_vertical":
                width = max(video_a.width, video_b.width)
                height = max(video_a.height, video_b.height)
            case "split_half_horizontal":
                width = max(video_a.width, video_b.width)
                height = max(video_a.height, video_b.height)
            case _:
                msg = f"Unsupported comparison mode: {mode}"
                raise ValueError(msg)

        return width, height

    @staticmethod
    def create_canvas(
        video_a: VideoMetadata,
        video_b: VideoMetadata,
        mode: str,
        background_color: str  # color como string "#RRGGBB"
    ) -> np.ndarray:
        width, height = Canvas.dimensions_canvas(video_a, video_b, mode)
        rgb_color = hex_to_rgb(background_color)

        return np.full((height, width, 3), rgb_color, dtype=np.uint8)

    @staticmethod
    def add_overlay_text(
        frame_a: np.ndarray,
        frame_b: np.ndarray,
        video_a: VideoMetadata,
        video_b: VideoMetadata,
        mode: str
    ) -> np.ndarray:
        match mode:
            case "side_by_side" | "top_bottom":
                frame_a = put_text(frame_a, video_a, "bottom_left")
                frame_b = put_text(frame_b, video_b, "bottom_left")
            case "split_half_vertical":
                frame_a = put_text(frame_a, video_a, "bottom_left")
                frame_b = put_text(frame_b, video_b, "bottom_right")
            case "split_half_horizontal":
                frame_a = put_text(frame_a, video_a, "top_left")
                frame_b = put_text(frame_b, video_b, "bottom_left")
            case _:
                msg = f"Unsupported mode for overlay text: {mode}"
                raise ValueError(msg)

        return frame_a, frame_b

    @staticmethod
    def compose_on_canvas(
        canvas: np.ndarray,
        frame_a: np.ndarray,
        frame_b: np.ndarray,
        mode: ModeType
    ) -> np.ndarray:
        canvas_h, canvas_w = canvas.shape[:2]

        if mode == "side_by_side":
            half_w = canvas_w // 2
            frame_a_resized = cv2.resize(frame_a, (half_w, canvas_h))
            frame_b_resized = cv2.resize(frame_b, (canvas_w - half_w, canvas_h))

            canvas[:, :half_w] = frame_a_resized
            canvas[:, half_w:] = frame_b_resized

        elif mode == "top_bottom":
            half_h = canvas_h // 2
            frame_a_resized = cv2.resize(frame_a, (canvas_w, half_h))
            frame_b_resized = cv2.resize(frame_b, (canvas_w, canvas_h - half_h))

            canvas[:half_h, :] = frame_a_resized
            canvas[half_h:, :] = frame_b_resized

        elif mode == "split_half_vertical":
            frame_a_resized = cv2.resize(frame_a, (canvas_w, canvas_h))
            frame_b_resized = cv2.resize(frame_b, (canvas_w, canvas_h))

            canvas[:, : canvas_w // 2] = frame_a_resized[:, : canvas_w // 2]
            canvas[:, canvas_w // 2 :] = frame_b_resized[:, canvas_w // 2 :]

            cv2.line(
                canvas,
                (canvas_w // 2, 0),
                (canvas_w // 2, canvas_h),
                color=(255, 255, 255),
                thickness=1
            )

        elif mode == "split_half_horizontal":
            frame_a_resized = cv2.resize(frame_a, (canvas_w, canvas_h))
            frame_b_resized = cv2.resize(frame_b, (canvas_w, canvas_h))

            canvas[: canvas_h // 2, :] = frame_a_resized[: canvas_h // 2, :]
            canvas[canvas_h // 2 :, :] = frame_b_resized[canvas_h // 2 :, :]

            cv2.line(
                canvas,
                (0, canvas_h // 2),
                (canvas_w, canvas_h // 2),
                color=(255, 255, 255),
                thickness=1
            )

        else:
            msg = f"Not supported: {mode}"
            raise ValueError(msg)

        return canvas
