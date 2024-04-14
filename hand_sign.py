import cv2
import time
import mediapipe as mp 
from config_manager import config


class Camera:
    def __init__(self):
        self.camera_index = 0
        self.camera_feed = cv2.VideoCapture(self.camera_index)

    def capture_frame(self, orientation, flip_direction, frame_format):

        isFrameRead = self.camera_feed.read()[0]

        if isFrameRead:

            frames = self.camera_feed.read()[1]
            frames = self._rotate_frame(frames, orientation)
            frames = self._flip_frames(frames, flip_direction)
            frames,rgb_frames = self._change_color_space(frames, frame_format)
            processed_frames = frames
            processed_frames_rgb = rgb_frames

            return processed_frames, processed_frames_rgb
        else:
            self._empty_frames()

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

        converted_frames_rgb = cv2.cvtColor(frames, cv2.COLOR_BGR2RGB)

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

        return converted_frames, converted_frames_rgb

    @staticmethod
    def _empty_frames():
       raise RuntimeError("No frames were read from the camera. Please check your device.")


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

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=config["use_static_mode"],
        max_num_hands=config["max_hands_count"],
        min_detection_confidence=config["min_detection_threshold"],
        min_tracking_confidence=config["min_tracking_threshold"],
    )
    mp_drawing = mp.solutions.drawing_utils

    while process_cycle:
        frames,rgb_frames = webcam.capture_frame(config["orientation"], config["flip_direction"], config["frame_format"])

        
        hand_landmarks = hands.process(rgb_frames)

        if hand_landmarks.multi_hand_landmarks:
            for hand_landmarks in hand_landmarks.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frames,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
                )

        process_cycle = show_root_window(frames)
        fps, previous_time = calculate_fps(previous_time)
        print(f"fps : {fps}")


if __name__ == "__main__":
    main()
