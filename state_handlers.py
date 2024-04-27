class StateManager:
    def __init__(self) -> None:
        self.server_state_map = {
            "start": self.start(),
            "stop": self.stop(),
            "terminate": self.terminate(),
            "idle": self.idle()
        }

        self.server_state = self.server_state_map.get("state", 'stop')


    def manage(self):
        while True:
            if self.server_state == "start":
                print("starting server process cycle")

            elif self.server_state == "stop":
                print("stopping process cycle")

            elif self.server_state == "terminate":
                print("closing api endpoint's")
                print("stopping process cycle")
                print("exiting...")

            elif self.server_state == "idle":
                print("api endpoint active")
            else:
                print("invalid state")

    def start(self):
        ...

    def stop(self):
        ...

    def terminate(self):
        ...

    def idle(self):
        ...

