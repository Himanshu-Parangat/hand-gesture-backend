from enum import Enum
import json


class config_options(str,Enum):
    CAMERA_PROPERTIES = "camera_properties"
    FRAMES = "frames"
    HANDTRACKING = "handTracking"


class ServerState(Enum):    
    IDLE = "idle",
    START = "start",
    STOP = "stop",
    TERMINATE = "terminate"
    

with open('./config/default_config.json', 'r') as file:
    default_config = json.load(file)

with open('./config/user_config.json', 'r') as file:
    user_config = json.load(file)



if __name__ == "__main__":
   print(default_config) 
