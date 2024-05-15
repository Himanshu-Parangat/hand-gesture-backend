from enum import Enum
from pydantic import BaseModel
from .config_handlers import default_config, user_config


class ServerState(Enum):    
    IDLE = "idle",
    START = "start",
    STOP = "stop",
    TERMINATE = "terminate"


class HandTracking(BaseModel):
    USE_STATIC_MODE: bool   
    MAX_HANDS_COUNT: int  
    MIN_DETECTION_THRESHOLD: float   
    MIN_TRACKING_THRESHOLD: float  


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

    NONE = "None"
    BGR = "BGR"
    RGB = "RGB"
    HSV = "HSV"
    HLS = "HLS"
    GRAY = "GRAY"


class Frames(BaseModel):
    ORIENTATION: FrameOrientation 
    FLIP_DIRECTION: FrameFlip 
    FRAME_FORMAT: FrameFormat 


class Camera_properties(BaseModel):
    DEFAULT_CAMERA: int
    FRAME_WIDTH: int
    FRAME_HEIGHT: int
    FPS: int
    BRIGHTNESS: int
    CONTRAST: int
    SATURATION: int
    HUE: int
    GAIN: int
    EXPOSURE: int


class config_options(str,Enum):
    CAMERA_PROPERTIES = "camera_properties"
    FRAMES = "frames"
    HANDTRACKING = "handTracking"


class base_config(BaseModel):
    handTracking: HandTracking
    frames: Frames
    camera_properties: Camera_properties 


def model_gen(config_data):
    config_model = base_config(**config_data)
    return config_model


default_model = model_gen(default_config) 
user_model= model_gen(user_config) 
