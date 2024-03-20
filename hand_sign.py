from typing import Any
import cv2
import mediapipe  


def initialize_camera(camera_index:int = 0) -> cv2.VideoCapture:
    cam = cv2.VideoCapture(camera_index)
    # cam.set(cv2.CAP_PROP_FPS, 60)
    return cam


def capture_camera(cam_state: bool) -> Any:
    cam = initialize_camera()
    hands = initialize_mediapipe()

    while cam_state:
        _ , img = cam.read() 
        img = cv2.flip(img,1)
        rgb_img = convert_img(img,'rgb')

        hands_landmarks = hands.process(rgb_img)
        print(hands_landmarks.multi_hand_landmarks)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


def convert_img(img: Any, img_format: str ) -> Any:
    if img_format.lower() == 'bgr':
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    elif img_format.lower() == 'rgb':
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else:
        raise ValueError("Unsupported img_format. expect either 'bgr' or 'rgb' ")


def initialize_mediapipe() -> Any:
    mpHands = mediapipe.solutions.hands
    hands = mpHands.Hands()
    return hands


def main() -> None:
    capture_camera(True)


if __name__ == "__main__":
    main()
