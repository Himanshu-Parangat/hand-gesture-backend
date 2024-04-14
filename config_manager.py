from enum import Enum

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

# inject for hand_sign.py
default_config = {
    "use_static_mode": False,  # live-mode
    "max_hands_count": 2,
    "min_detection_threshold": 0.5,
    "min_tracking_threshold": 0.5,
    "orientation": FrameOrientation.ZERO_DEGREE.value,
    "flip_direction": FrameFlip.HORIZONTALLY.value,
    "frame_format": FrameFormate.BGR.value,
}

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
config = default_config
