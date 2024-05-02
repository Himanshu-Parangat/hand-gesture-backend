from fastapi import FastAPI, Body, HTTPException
from config_handlers import config_options
from pydantic import BaseModel
from config_handlers import default_config, user_config
from enum import Enum



app = FastAPI()


@app.get("/ping")
async def status():
    return {"status": "active"}


@app.post("/ping")
async def ping(data: dict = Body(...)):
    """
    Checks if client, is alive? and sending status at regular intervl

    Raises a 422 Unprocessable Entity error if the request body is not a dictionary.
    """

    if data != {"status": "alive"}:
        raise HTTPException(status_code=404, detail=f"expected format is  'status':'your status' ")

    return {"message": "resetting the internal timer"}




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


class base_config(BaseModel):
    handTracking: HandTracking
    frames: Frames
    camera_properties: Camera_properties 



config = base_config.model_validate(default_config)


@app.get("/server/config/default")
def get_default_config() -> base_config: 
    """
    get the default stored config for the server
    """
    return config


@app.post("/server/config/post")
def post_default_config(config: base_config = Body(...)) -> base_config: 
    """
    get the default stored config for the server
    """
    return config


@app.get("/server/config/default/{field}")
def get_default_config_field(field: config_options) -> dict:
    """
    From default config get specific field
    """

    field_entry = field.value
    field_value = default_config.get(field_entry)

    if field_entry is None:
        raise HTTPException(status_code=404, detail=f"no field with name {field}")
    return {"entry": field_entry, "value": field_value}



@app.get("/server/config/user")
def get_user_config() -> base_config:
    """
    get the stored user config from the server
    """
    return user_config


@app.get("/server/config/user/{field}")
def get_user_config_field(field: config_options) -> dict:
    """
    from user config get specific field
    """

    field_entry = field.value
    field_value = user_config.get(field_entry)

    if field_entry is None:
        raise HTTPException(status_code=404, detail=f"no field with name {field}")
    return {"entry": field_entry, "value": field_value}
