from asyncio import sleep
import asyncio
import cv2
from time import sleep
from datetime import datetime
from src.configuration import config
from src.tracking import Camera
from src.tracking import HandTracker
from src.endpoint.endpoint_handlers import app
import uvicorn

class ServerManager:
    def __init__(self) -> None:
        self.webcam = Camera()
        self.handtracker = HandTracker()
        self.server_state = True

    def process_cycle(self, state):

        while state:

            frames, rgb_frames = self.webcam.capture_frame(config("orientation"), config("flip_direction"), config("frame_format"))
            marks = self.handtracker.landmark(rgb_frames)

            print(marks)
            self.show_root_window(frames)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                cv2.destroyAllWindows()
                self.server_state = False
                break

    def show_root_window(self, display_frames, window_name: str = "frames"):
        cv2.imshow(window_name, display_frames)

def run_detection():

    detectin = ServerManager()
    while True:
        detectin.process_cycle(True)


def log_info():
    while True:
        formatted_time = datetime.now().strftime("%H-%M-%S")
        print(f"[{formatted_time}] Running backend...")
        sleep(0.5)

def non_blocking_function():
    uvicorn.run(app, host="0.0.0.0", port=8000)

def main():
    print("starting application...")

    while True:
        detection_task = asyncio.create_task(run_detection())
        log_task = asyncio.create_task(log_info())


if __name__ == "__main__":
    asyncio.run(main())

