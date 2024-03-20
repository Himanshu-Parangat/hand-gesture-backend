from typing import Any
import cv2

def inatialize_camera(cameraImdex:int = 0) -> cv2.VideoCapture:
    cam = cv2.VideoCapture(cameraImdex)
    cam.set(cv2.CAP_PROP_FPS, 60)
    return cam

def capture_camera(cam_state: bool) -> Any:
    cam = inatialize_camera()
    while cam_state:
        _ , img = cam.read() 
        conv_img = convert_img(img,'rgb')
        cv2.imshow("Image", conv_img)
        cv2.waitKey(1)

def convert_img(img: Any, format: str ) -> Any:
    if format.lower() == 'bgr':
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    elif format.lower() == 'rgb':
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else:
        raise ValueError("Unsupported format. Please choose either 'bgr' or 'rgb'.")

def main() -> None:
    capture_camera(True)


if __name__ == "__main__":
    main()
