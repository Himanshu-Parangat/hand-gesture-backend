from fastapi import FastAPI, Path, Query 
from config_handlers import FrameFormate, FrameOrientation, FrameFlip



app = FastAPI()


@app.get("/")
async def root():
    return {"message": "server under construction.."}


default_config = {
    "use_static_mode": False,  # live-mode
    "max_hands_count": 2,
    "min_detection_threshold": 0.5,
    "min_tracking_threshold": 0.5,
    "orientation": "" ,
    "flip_direction": "",
    "frame_format": "",
}


@app.get("/server/defaultConfig")
async def get_default_config():
    return default_config


@app.get("/server/defaultConfig/{field}")
async def get_field(field: str = Path(description="the configration field")):
    field_data = default_config.get(field, "unexpected option requsted")
    return field_data



@app.get("/server/config/")
def get_config(
    orientation: FrameOrientation = Query(..., description="Frame orientation"),
    flip: FrameFlip = Query(..., description="Frame flip"),
    format: FrameFormate = Query(..., description="Frame format")
):
    return {
        "orientation": orientation,
        "flip": flip,
        "format": format
    }

