from fastapi import FastAPI, Body, HTTPException
from model_handlers import config_options
from model_handlers import default_config, user_config
from model_handlers import base_config, config_model


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


@app.post("/server/config/user")
def post_default_config(config: base_config = Body(...)) -> base_config: 
    """
    get the default stored config for the server
    """
    return config


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


@app.get("/server/config/default")
def get_default_config() -> base_config: 
    """
    get the default stored config for the server
    """
    return config_model


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
