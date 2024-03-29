from typing import Any
import cv2
import mediapipe
import numpy
import time

config = {
    'live_video_mode': False,
    'min_detection_threshold': 0.5,
    'min_tracking_threshold': 0.5,
    'default_camera_index': 0,
    'camera_flip_direction': "Flipcode",
    'available_camera_flip_directions': ["top", "bottom", "left", "right"],
    'available_frame_formats': ["BGR", "RGB"],
    'max_hands_count': 2,
    'visualizations_to_show': ["mask", "dots", "Connections", "outline"]
}


class Landmark:
    def __init__(self):
        self.mp_hands = mediapipe.solutions.hands.Hands(
            static_image_mode=config['live_video_mode'],
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


class Camera:
    def __init__(self):
        self.camera_index = 0
        self.camera_feed = cv2.VideoCapture(self.camera_index)
        self.inverted_frames = None

    def capture_raw_flipped_frames(self) -> numpy.ndarray:
        self.inverted_frames = self.camera_feed.read()[1]
        return self.inverted_frames

    def capture_frame(self) -> numpy.ndarray:
        inverted_frames = self.capture_raw_flipped_frames()
        frames = cv2.flip(inverted_frames, 1)
        return frames

    @staticmethod
    def convert_frames_to_RGB(input_frames) -> numpy.ndarray:
        return cv2.cvtColor(input_frames, cv2.COLOR_BGR2RGB)

    @staticmethod
    def convert_frames_to_BGR(input_frames) -> numpy.ndarray:
        return cv2.cvtColor(input_frames, cv2.COLOR_RGB2BGR)


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
    landmark = Landmark()
    # fps initialise time
    previous_time = time.time()

    while process_cycle:
        frames = webcam.capture_frame()
        rgb_frames = webcam.convert_frames_to_RGB(frames)
        landmark_obj = Landmark.get_mediapipe_landmark(rgb_frames, landmark.mp_hands)

        result_frames = landmark.draw_mediapipe_landmark(frames, landmark_obj)
        process_cycle = show_root_window(result_frames)
        fps, previous_time = calculate_fps(previous_time)
        print(f"fps : {fps}")


if __name__ == "__main__":
    main()
