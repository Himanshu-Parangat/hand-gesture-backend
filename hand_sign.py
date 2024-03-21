from typing import Any
import cv2
import mediapipe  


def initialize_camera(camera_index:int = 0) -> cv2.VideoCapture:
    captured = cv2.VideoCapture(camera_index)
    # cam.set(cv2.CAP_PROP_FPS, 60)
    return captured


def capture_frame(camera_feed: cv2.VideoCapture) -> Any :
    _ , inverted_frames = camera_feed.read() 
    frames = cv2.flip(inverted_frames,1)
    return frames


def convert_format(img: Any, img_format: str ) -> Any:
    if img_format.lower() == 'bgr':
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    elif img_format.lower() == 'rgb':
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
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



def main(capture_state: bool) -> None:
    capture = initialize_camera() 
    hands = initialize_mediapipe()

    while (capture_state):
        
        cam = capture_frame(capture)

        rgb_img = convert_format(cam,'rgb')
        hands_landmarks = hands.process(rgb_img)
        
        print(hands_landmarks.multi_hand_landmarks)
        cv2.imshow("Image", cam)
        cv2.waitKey(1)

if __name__ == "__main__":
    main(True)
