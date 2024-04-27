import mediapipe as mp 
from config_handlers import config


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

    def _iterate_seprate_hands(self, hand_landmarks):

        if hand_landmarks.multi_hand_landmarks:
            for hands_mark in hand_landmarks.multi_hands_mark:
                for idx, landmark in enumerate(hands_mark.landmark):
                    if idx == mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP.value:
                        if hands_mark.handedness == mp.solutions.hands.HandedNess.LEFT:
                            left_index_x = landmark.x
                            left_index_y = landmark.y
                            print(f"Left Index Finger: ({left_index_x}, {left_index_y})")
                        else:
                            right_index_x = landmark.x
                            right_index_y = landmark.y
                            print(f"Right Index Finger: ({right_index_x}, {right_index_y})")


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


