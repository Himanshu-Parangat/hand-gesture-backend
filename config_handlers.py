from enum import Enum
from pydantic import BaseModel, json

class FrameOrientation(Enum):
    """possible value: "None" "clockwise" "180"  "counter-clockwise" """

    CLOCKWISE = "clockwise"
    COUNTER_CLOCKWISE = "counter_clockwise"
    ZERO_DEGREE = "0"
    ONE_EIGHTY_DEGREE = "180"


class FrameFlip(Enum):
    """possible value:  "None" "horizontally" "vertically" "both" """

    NONE: str = "None"
    HORIZONTALLY: str = "horizontally"
    VERTICALLY: str = "vertically"
    BOTH: str = "both"


class FrameFormate(Enum):
    """possible value: "None" "BGR" "RGB" "HSV" "HLS" "Gray" """

    BGR: str = "BGR"
    RGB: str = "RGB"
    HSV: str = "HSV"
    HLS: str = "HLS"
    GRAY: str = "GRAY"

class Frames(Enum):
    ORIENTATION = FrameOrientation.ZERO_DEGREE.value
    FLIP_DIRECTION = FrameFlip.HORIZONTALLY.value
    FRAME_FORMAT = FrameFormate.BGR.value


class Camera_properties(Enum):
    DEFAULT_CAMERA: int = 0,
    FRAME_WIDTH: int = 640,
    FRAME_HEIGHT: int = 480,
    FPS: int = 5,
    BRIGHTNESS: int = 10,
    CONTRAST: int = 11,
    SATURATION: int = 12,
    HUE: int = 13,
    GAIN: int = 14,
    EXPOSURE: int = 15

class ServerState(Enum):    
    IDLE = "idle",
    START = "start",
    STOP = "stop",
    TERMINATE = "terminate"


class HandTracking(Enum):
    USE_STATIC_MODE: bool = False  # live-mode
    MAX_HANDS_COUNT: int = 2
    MIN_DETECTION_THRESHOLD: float = 0.5
    MIN_TRACKING_THRESHOLD:float = 0.5


class DefaultConfig(BaseModel):
    SERVERSTATE: ServerState
    HANDTRACKING: HandTracking
    FRAMES: Frames
    CAMERA_PROPERTIES: Camera_properties



# Generate JSON Schema
json_schema = DefaultConfig.model_json_schema()

# Print JSON Schema
print(json_schema)

production_config = {
    "use_static_mode": False,  # live-mode
    "max_hands_count": 2,
    "min_detection_threshold": 0.5,
    "min_tracking_threshold": 0.5,
    "orientation": FrameOrientation.ZERO_DEGREE.value,
    "flip_direction": FrameFlip.HORIZONTALLY.value,
    "frame_format": FrameFormate.BGR.value,
}



# use this 
# config = default_config
