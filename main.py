import cv2
from config_handlers import config
from camera_handlers import Camera
from handtracker_handlers import HandTracker


class ServerManager:
    def __init__(self) -> None:
        self.webcam = Camera()
        self.handtracker = HandTracker()
        self.server_state = True

    def process_cycle(self,state):

        while state:
            frames,rgb_frames = self.webcam.capture_frame(config("orientation"), config("flip_direction"), config("frame_format"))

            marks = self.handtracker.landmark(rgb_frames)
            print(marks)

            self.show_root_window(frames)


    def show_root_window(self, display_frames, window_name: str = "frames"):
        cv2.imshow(window_name, display_frames)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            cv2.destroyAllWindows()
            self.server_state = False


class ProjectController:
    def __init__(self):
        self.should_run = True

    def run(self):
        Server = ServerManager()
        while self.should_run:
            state = Server.server_state  

            Server.process_cycle(state)


if __name__ == "__main__":
    runner = ProjectController()
    runner.run()
