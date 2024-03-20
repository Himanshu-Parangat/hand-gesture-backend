import cv2

def inatialize_camera(cameraImdex:int = 0) -> cv2.VideoCapture:
    cam = cv2.VideoCapture(cameraImdex)
    return cam

def capture_camera(cam_state: bool) -> None:
    cam = inatialize_camera()
    while cam_state:
        success, img = cam.read() 

        cv2.imshow("Image", img)
        cv2.waitKey(1)

def main() -> None:
    capture_camera(True)


if __name__ == "__main__":
    main()
