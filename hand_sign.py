from typing import Any, Dict
import cv2
import mediapipe
import numpy
import time

config: dict[str, bool | float | str | int] = {
    'use_static_mode': False,  # live-mode
    'max_hands_count': 2,
    'min_detection_threshold': 0.5,
    'min_tracking_threshold': 0.5,
    'orientation': "0",  # "None" "clockwise" "180"  "counter-clockwise"
    'flip_direction': "horizontally",  # "None" "horizontally" "vertically" "both"
    'frame_format': "BGR"  # "None" "BGR" "RGB" "HSV" "HLS" "Gray"
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
        elif frame_format == "Gray":
            converted_frames = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
        else:
            converted_frames = frames

        return converted_frames

    @staticmethod
    def _empty_frames(self):
        return "no frames are read, check your device"


class Landmark:
    def __init__(self):
        self.mp_hands = mediapipe.solutions.hands.Hands(
            static_image_mode=config['use_static_mode'],
            max_num_hands=config['max_hands_count'],
            min_detection_confidence=config['min_detection_threshold'],
            min_tracking_confidence=config['min_tracking_threshold']
        )
        self.mpDraw = mediapipe.solutions.drawing_utils

    @staticmethod
    def get_mediapipe_landmark(camera_feed: cv2.VideoCapture | numpy.ndarray, mp_hands) -> Any:
        hands_landmarks = mp_hands.process(camera_feed)

        return hands_landmarks

    def draw_mediapipe_landmark(self, input_bgr_frames: numpy.ndarray, result_frames: Any):
        if result_frames.multi_hand_landmarks:
            for handLms in result_frames.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(input_bgr_frames, handLms, mediapipe.solutions.hands.HAND_CONNECTIONS)
        return input_bgr_frames


def calculate_fps(previous_time: float) -> tuple[int, float]:
    current_time = time.time()
    fps = int(1 / (current_time - previous_time))
    return fps, current_time


def show_root_window(display_frames, window_name: str = "frames"):
    cv2.imshow(window_name, display_frames)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        cv2.destroyAllWindows()
        return False
    return True


def main():
    process_cycle = True
    webcam = Camera()
    previous_time = time.time()

    while process_cycle:
        frames = webcam.capture_frame(config['orientation'], config['flip_direction'], config['frame_format'])
        process_cycle = show_root_window(frames)
        fps, previous_time = calculate_fps(previous_time)
        print(f"fps : {fps}")


if __name__ == "__main__":
    main()
