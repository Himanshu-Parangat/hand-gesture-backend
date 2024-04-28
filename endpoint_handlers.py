from fastapi import FastAPI, Path, Query 
from config_handlers import default_config, FrameFormate, FrameOrientation, FrameFlip



app = FastAPI()


@app.get("/")
async def root():
    return {"message": "server under construction.."}


@app.get("/server/defaultConfig")
async def get_default_config():
    return default_config


@app.get("/server/defaultConfig/{field}")
async def get_field(field: str = Path(description="the configration field")):
    field_data = default_config.get(field, "unexpected option requsted")
    return field_data



@app.get("/server/config/")
def get_config(
    use_static_mode: bool = Query(False, description="enable static mode?"),  
    max_hands_count: int =  Query(2, description="numer of max hands", ge=0, le=2),
    min_detection_threshold: float = Query(0.5, description= "model minimum detection threshold", ge=0.0, le=1.0),
    min_tracking_threshold: float = Query(0.5, description= "model minimum tracking threshold", ge=0.0, le=1.0),
    orientation: FrameOrientation = Query(..., description="Frame orientation"),
    flip: FrameFlip = Query(..., description="Frame flip"),
    format: FrameFormate = Query(..., description="Frame format")

    ):
    user_config = {
        "use_static_mode": use_static_mode,  # live-mode
        "max_hands_count": max_hands_count,
        "min_detection_threshold": min_detection_threshold,
        "min_tracking_threshold": min_tracking_threshold,
        "orientation": orientation,
        "flip": flip,
        "format": format
    }
    return user_config

