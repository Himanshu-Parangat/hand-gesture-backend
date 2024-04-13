import cv2
import time
from enum import Enum

class FrameOrientation(Enum):
    """possible value: "None" "clockwise" "180"  "counter-clockwise" """

    CLOCKWISE = "clockwise"
    COUNTER_CLOCKWISE = "counter_clockwise"
    ZERO_DEGREE = "0"
    ONE_EIGHTY_DEGREE = "180"


class FrameFlip(Enum):
    """possible value:  "None" "horizontally" "vertically" "both" """

    NONE: str = "None"
    HORIZONTALLY: str = "horizontally"
    VERTICALLY: str = "vertically"
    BOTH: str = "both"


class FrameFormate(Enum):
    """possible value: "None" "BGR" "RGB" "HSV" "HLS" "Gray" """

    BGR: str = "BGR"
    RGB: str = "RGB"
    HSV: str = "HSV"
    HLS: str = "HLS"
    GRAY: str = "GRAY"


config = {
    "use_static_mode": False,  # live-mode
    "max_hands_count": 2,
    "min_detection_threshold": 0.5,
    "min_tracking_threshold": 0.5,
    "orientation": FrameOrientation.ZERO_DEGREE.value,
    "flip_direction": FrameFlip.HORIZONTALLY.value,
    "frame_format": FrameFormate.RGB.value,
}


class Camera:
    def __init__(self):
        self.camera_index = 0
        self.camera_feed = cv2.VideoCapture(self.camera_index)

    def capture_frame(self, orientation, flip_direction, frame_format):
        frames = self.camera_feed.read()[1]
        frames = self._rotate_frame(frames, orientation)
        frames = self._flip_frames(frames, flip_direction)
        frames = self._change_color_space(frames, frame_format)
        processed_frames = frames

        return processed_frames

    @staticmethod
    def _rotate_frame(frames, orientation):
        if orientation == "clockwise":
            rotated_frames = cv2.rotate(frames, cv2.ROTATE_90_CLOCKWISE)
        elif orientation == "180":
            rotated_frames = cv2.rotate(frames, cv2.ROTATE_180)
        elif orientation == "counter-clockwise":
            rotated_frames = cv2.rotate(frames, cv2.ROTATE_90_COUNTERCLOCKWISE)
        else:
            rotated_frames = frames

        return rotated_frames

    @staticmethod
    def _flip_frames(frames, flip_direction):
        if flip_direction == "horizontally":
            flipped_frames = cv2.flip(frames, 1)
        elif flip_direction == "vertically":
            flipped_frames = cv2.flip(frames, 0)
        elif flip_direction == "both":
            flipped_frames = cv2.flip(frames, -1)
        else:
            flipped_frames = frames

        return flipped_frames

    @staticmethod
    def _change_color_space(frames, frame_format):
        if frame_format == "BGR":
            converted_frames = frames
        elif frame_format == "RGB":
            converted_frames = cv2.cvtColor(frames, cv2.COLOR_BGR2RGB)
        elif frame_format == "HSV":
            converted_frames = cv2.cvtColor(frames, cv2.COLOR_BGR2HSV)
        elif frame_format == "HLS":
            converted_frames = cv2.cvtColor(frames, cv2.COLOR_BGR2HLS)
        elif frame_format == "GRAY":
            converted_frames = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
        else:
            converted_frames = frames

        return converted_frames

    @staticmethod
    def _empty_frames():
        return "no frames are read, check your device"


def calculate_fps(previous_time: float) -> tuple[int, float]:
    current_time = time.time()
    fps = int(1 / (current_time - previous_time))
    return fps, current_time


def show_root_window(display_frames, window_name: str = "frames"):
    cv2.imshow(window_name, display_frames)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        cv2.destroyAllWindows()
        return False
    return True


def main():
    process_cycle = True
    webcam = Camera()
    previous_time = time.time()

    while process_cycle:
        frames = webcam.capture_frame(config["orientation"], config["flip_direction"], config["frame_format"])
        process_cycle = show_root_window(frames)
        fps, previous_time = calculate_fps(previous_time)
        print(f"fps : {fps}")


if __name__ == "__main__":
    main()
