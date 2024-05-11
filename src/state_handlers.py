import cv2
import uvicorn
from threading import Thread
from .config.config_handlers import config
from .detection.camera_handlers import Camera
from .detection.handtracker_handlers import HandTracker


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

            # Check for 'q' key press here
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                cv2.destroyAllWindows()
                self.server_state = False
                break  # Exit the loop

    def show_root_window(self, display_frames, window_name: str = "frames"):
        cv2.imshow(window_name, display_frames)


class EndpointManager:
    def __init__(self) -> None:
        self.endpoint_state = True

    def process_cycle(self, state):
        while state:
            uvicorn.run("endpoint_handlers:app", host="0.0.0.0", port=8000, reload=True)

            break


# class ProjectController:
#     def __init__(self):
#         self.should_run = True
#
#     def run(self):
#
#         Server = ServerManager()
#         Endpoint = EndpointManager() 
#
#         while self.should_run:
#             state = Server.server_state  
#
#             print("server in running")
#             Server.process_cycle(state)
#             Endpoint.process_cycle(state)
#             break

class ProjectController:
    def __init__(self):
        self.should_run = True

    def run(self):
        Server = ServerManager()
        Endpoint = EndpointManager()

        endpoint_thread = Thread(target=Endpoint.process_cycle, args=(Endpoint.endpoint_state,))
        # server_thread = Thread(target=Server.process_cycle, args=(Server.server_state,))

        endpoint_thread.start()
        # server_thread.start()

        endpoint_thread.join()
        # server_thread.join()


if __name__ == "__main__":
    runner = ProjectController()
    runner.run()

def main():
    print("starting application...")

