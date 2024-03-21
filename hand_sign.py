from typing import Any
import cv2
import mediapipe
import numpy


def initialize_camera(camera_index:int = 0) -> cv2.VideoCapture:
    camera_feed = cv2.VideoCapture(camera_index)
    # cam.set(cv2.CAP_PROP_FPS, 60)
    return camera_feed


def capture_frame(camera_feed: cv2.VideoCapture) -> numpy.ndarray :
    _ , inverted_frames = camera_feed.read() 
    frames = cv2.flip(inverted_frames,1)
    return frames


def convert_format(frames: Any, img_format: str ) -> Any:
    if img_format.lower() == 'bgr':
        return cv2.cvtColor(frames, cv2.COLOR_RGB2BGR)
    elif img_format.lower() == 'rgb':
        return cv2.cvtColor(frames, cv2.COLOR_BGR2RGB)
    else:
        raise ValueError("Unsupported img_format. expect either 'bgr' or 'rgb' ")


def initialize_mediapipe() -> mediapipe.solutions.hands.Hands:
    mp_hands = mediapipe.solutions.hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    return mp_hands


def mediapipe_landmark(camera_feed: cv2.VideoCapture,mp_hands) -> Any:
    bgr_frames = capture_frame(camera_feed)

    rgb_frames = convert_format(bgr_frames,'rgb')
    hands_landmarks = mp_hands.process(rgb_frames)
    
    return hands_landmarks,bgr_frames


def draw_hand_landmarks(bgr_frames: numpy.ndarray, result_frames: Any) -> numpy.ndarray:
    mpDraw = mediapipe.solutions.drawing_utils
    if result_frames.multi_hand_landmarks:
        for handLms in result_frames.multi_hand_landmarks:
            mpDraw.draw_landmarks(bgr_frames, handLms, mediapipe.solutions.hands.HAND_CONNECTIONS)
    return bgr_frames



def main(process_cycle: bool) -> None:
    camera_feed = initialize_camera() 
    mp_hands = initialize_mediapipe()

    while process_cycle:
        landmarked_frames,bgr_frames = mediapipe_landmark(camera_feed,mp_hands)
        connected_landmarked_frames = draw_hand_landmarks(bgr_frames,landmarked_frames)

        cv2.imshow("Image", connected_landmarked_frames)
        cv2.waitKey(1)

if __name__ == "__main__":
    main(True)
