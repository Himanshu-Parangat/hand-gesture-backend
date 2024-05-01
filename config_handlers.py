from enum import Enum
from pydantic import BaseModel


class config_options(str,Enum):
    CAMERA_PROPERTIES = "camera_properties"
    FRAMES = "frames"
    HANDTRACKING = "handTracking"

class Camera_properties(int, Enum):
    DEFAULT_CAMERA = 0
    FRAME_WIDTH = 640
    FRAME_HEIGHT = 480
    FPS = 5
    BRIGHTNESS = 10
    CONTRAST = 11
    SATURATION = 12
    HUE = 13
    GAIN = 14
    EXPOSURE = 15


class FrameOrientation(str,Enum):
    """possible value: "None" "clockwise" "180"  "counter-clockwise" """

    NONE = "None"
    CLOCKWISE = "clockwise"
    COUNTER_CLOCKWISE = "counter_clockwise"
    ZERO_DEGREE = "0"
    ONE_EIGHTY_DEGREE = "180"


class FrameFlip(str, Enum):
    """possible value: "None" "horizontally" "vertically" "both" """

    NONE = "None"
    HORIZONTALLY = "horizontally"
    VERTICALLY = "vertically"
    BOTH = "both"

class FrameFormat(str, Enum):
    """possible value: "None" "BGR" "RGB" "HSV" "HLS" "Gray" """

    BGR = "BGR"
    RGB = "RGB"
    HSV = "HSV"
    HLS = "HLS"
    GRAY = "GRAY"



class Frames(BaseModel):
    ORIENTATION: FrameOrientation 
    FLIP_DIRECTION: FrameFlip 
    FRAME_FORMAT: FrameFormat 




# class HandTracking(BaseModel):
#     USE_STATIC_MODE: bool = False  # live-mode
#     MAX_HANDS_COUNT: conint(ge=1, le=2)  
#     MIN_DETECTION_THRESHOLD: confloat(ge=0.0, le=1.0)   
#     MIN_TRACKING_THRESHOLD: confloat(ge=0.0, le=1.0)  



class ServerState(Enum):    
    IDLE = "idle",
    START = "start",
    STOP = "stop",
    TERMINATE = "terminate"
    

class DefaultConfig(BaseModel):
    # HANDTRACKING: HandTracking
    FRAMES: Frames
    CAMERA_PROPERTIES: Camera_properties
    SERVERSTATE: ServerState




production_config = {
    "use_static_mode": False,  # live-mode
    "max_hands_count": 2,
    "min_detection_threshold": 0.5,
    "min_tracking_threshold": 0.5,
    "orientation": FrameOrientation.ZERO_DEGREE.value,
    "flip_direction": FrameFlip.HORIZONTALLY.value,
    # "frame_format": FrameFormate.BGR.value,
}


if __name__ == "__main__":
   schema = DefaultConfig.model_json_schema()
   print(schema) 
