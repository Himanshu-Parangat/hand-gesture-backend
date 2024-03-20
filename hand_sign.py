from typing import Any
import cv2


def initialize_camera(cameraIndex:int = 0) -> cv2.VideoCapture:
    cam = cv2.VideoCapture(cameraIndex)
    cam.set(cv2.CAP_PROP_FPS, 60)
    return cam


def capture_camera(cam_state: bool) -> Any:
    cam = initialize_camera()
    while cam_state:
        _ , img = cam.read() 
        conv_img = convert_img(img,'rgb')
        cv2.imshow("Image", conv_img)
        cv2.waitKey(1)


def convert_img(img: Any, img_format: str ) -> Any:
    if img_format.lower() == 'bgr':
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    elif img_format.lower() == 'rgb':
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else:
        raise ValueError("Unsupported img_format. expect either 'bgr' or 'rgb' ")



def main() -> None:
    capture_camera(True)


if __name__ == "__main__":
    main()
