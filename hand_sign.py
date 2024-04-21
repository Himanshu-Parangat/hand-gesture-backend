import cv2
import time
import mediapipe as mp 
from config_manager import config


class Camera:
    def __init__(self):
        self.camera_index = 0
        self.camera_feed = cv2.VideoCapture(self.camera_index)
        self.camera_feed.set(3, 640) 
        self.camera_feed.set(4, 480)

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


class HandTracker:
    def __init__(self):
        self.hand_solution = mp.solutions.hands
        self.hands = self.hand_solution.Hands(
            static_image_mode=config["use_static_mode"],
            max_num_hands=config["max_hands_count"],
            min_detection_confidence=config["min_detection_threshold"],
            min_tracking_confidence=config["min_tracking_threshold"],
        )

    def landmark(self, rgb_frames):
        marked_frame = self._process_landmark(rgb_frames)
        marked_frame = self._iterate_hands(marked_frame)

        if marked_frame is not None:
            marked_frame = self._get_landmark(marked_frame, "INDEX_FINGER_TIP")

        return marked_frame


    def _process_landmark(self,rgb_frames):
        hand_landmarks = self.hands.process(rgb_frames)
        return hand_landmarks


    @staticmethod
    def _iterate_hands(hand_landmarks):
        if hand_landmarks.multi_hand_landmarks:
            for landmarks_coord in hand_landmarks.multi_hand_landmarks:
                return landmarks_coord

    @staticmethod
    def _get_landmark(hand_landmarks, marks):
        landmarks = {
            "WRIST": hand_landmarks.landmark[0],

            "THUMB_CMC": hand_landmarks.landmark[1],
            "THUMB_MCP": hand_landmarks.landmark[2],
            "THUMB_IP": hand_landmarks.landmark[3],
            "THUMB_TIP": hand_landmarks.landmark[4],

            "INDEX_FINGER_MCP": hand_landmarks.landmark[5],
            "INDEX_FINGER_PIP": hand_landmarks.landmark[6],
            "INDEX_FINGER_DIP": hand_landmarks.landmark[7],
            "INDEX_FINGER_TIP": hand_landmarks.landmark[8],

            "MIDDLE_FINGER_MCP": hand_landmarks.landmark[9],
            "MIDDLE_FINGER_PIP": hand_landmarks.landmark[10],
            "MIDDLE_FINGER_DIP": hand_landmarks.landmark[11],
            "MIDDLE_FINGER_TIP": hand_landmarks.landmark[12],

            "RING_FINGER_MCP": hand_landmarks.landmark[13],
            "RING_FINGER_PIP": hand_landmarks.landmark[14],
            "RING_FINGER_DIP": hand_landmarks.landmark[15],
            "RING_FINGER_TIP": hand_landmarks.landmark[16],

            "PINKY_FINGER_MCP": hand_landmarks.landmark[17],
            "PINKY_FINGER_PIP": hand_landmarks.landmark[18],
            "PINKY_FINGER_DIP": hand_landmarks.landmark[19],
            "PINKY_FINGER_TIP": hand_landmarks.landmark[20]
        }

        requested_landmarks = {marks: landmarks[marks]}

        return requested_landmarks 

    @staticmethod
    def _get_coordinates(hand_landmarks, frames):
        """ normalized frames by frames size"""

        x_coordinates = int(hand_landmarks.x * frames.shape[1])
        y_coordinates = int(hand_landmarks.y * frames.shape[0])

        return x_coordinates, y_coordinates


class LandmarksDraw:
    def __init__(self):
        self.drawing_solution = mp.solutions.draw_landmarks
        self.hand_connections = self.hand_solution.HAND_CONNECTIONS

    def draw_landmarks(self, frames, hand_landmarks):
        drawn_frame = frames.copy()
        self.drawing_solution.draw_landmarks(
            drawn_frame,
            hand_landmarks,
            self.hand_connections,
            self.drawing_solution.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2),
            self.drawing_solution.DrawingSpec(color=(0, 0, 0), thickness=2)
        )
        return drawn_frame


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
    previous_time = time.time()
    webcam = Camera()
    handtracker = HandTracker() 

    while process_cycle:
        frames,rgb_frames = webcam.capture_frame(config["orientation"], config["flip_direction"], config["frame_format"])

        # frames,original_frames = handtracker.process_landmark(rgb_frames, frames)
        # l,r = handtracker.landmark(rgb_frames)
        #  
        # print(f"Left: {l}", f"Right: {r}")
        marks = handtracker.landmark(rgb_frames)
        print(marks)

        process_cycle = show_root_window(frames)
        fps, previous_time = calculate_fps(previous_time)
        # print(f"fps : {fps}")


if __name__ == "__main__":
    main()
