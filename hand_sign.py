from typing import Any
import cv2
import mediapipe
import numpy
import time


class landmark:
    def __init__(self,max_num_hands: int = 2):
        self.mp_hands = mediapipe.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )


# def mediapipe_landmark(camera_feed: cv2.VideoCapture, mp_hands) -> Any:
#     bgr_frames = capture_frame(camera_feed)
#
#     rgb_frames = convert_format(bgr_frames, 'rgb')
#     hands_landmarks = mp_hands.process(rgb_frames)
#
#     return hands_landmarks, bgr_frames

# def initialize_mediapipe() -> mediapipe.solutions.hands.Hands:
#     mp_hands = mediapipe.solutions.hands.Hands(
#         static_image_mode=False,
#         max_num_hands=2,
#         min_detection_confidence=0.5,
#         min_tracking_confidence=0.5
#     )
#     return mp_hands




# def draw_hand_landmarks(bgr_frames: numpy.ndarray, result_frames: Any) -> numpy.ndarray:
#     mpDraw = mediapipe.solutions.drawing_utils
#     if result_frames.multi_hand_landmarks:
#         for handLms in result_frames.multi_hand_landmarks:
#             mpDraw.draw_landmarks(bgr_frames, handLms, mediapipe.solutions.hands.HAND_CONNECTIONS)
#     return bgr_frames


# def main(process_cycle: bool) -> None:
#     camera_feed = initialize_camera()
#     mp_hands = initialize_mediapipe()
#
#     previous_time = time.time()
#     while process_cycle:
#         landmarked_frames, bgr_frames = mediapipe_landmark(camera_feed, mp_hands)
#         connected_landmarked_frames = draw_hand_landmarks(bgr_frames, landmarked_frames)
#
#         fps, previous_time = calculate_fps(previous_time)
#         print(f"fps : {fps}")
#
#         cv2.imshow("Image", connected_landmarked_frames)
#         cv2.waitKey(1)


class Camera:
    def __init__(self):
        self.camera_index = 0
        self.camera_feed = cv2.VideoCapture(self.camera_index)

    def capture_raw_flipped_frames(self) -> numpy.ndarray:
        self.inverted_frames = self.camera_feed.read()[1]
        return self.inverted_frames

    def capture_frame(self) -> numpy.ndarray:
        inverted_frames = self.capture_raw_flipped_frames()
        frames = cv2.flip(inverted_frames, 1)
        return frames

    @staticmethod
    def convert_frames_to_BRG(input_frames) -> numpy.ndarray:
        return cv2.cvtColor(input_frames, cv2.COLOR_BGR2RGB)

    @staticmethod
    def convert_frames_to_RGB(input_frames) -> numpy.ndarray:
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
    camera_feed = webcam.camera_feed
    previous_time = time.time()

    while process_cycle:
        # display_frames = webcam.capture_raw_flipped_frames()
        # display_frames = webcam.capture_frame()
        display_frames = webcam.convert_frames_to_BRG(webcam.capture_frame())

        process_cycle = show_root_window(display_frames)

        fps, previous_time = calculate_fps(previous_time)
        print(f"fps : {fps}")


if __name__ == "__main__":
    main()
