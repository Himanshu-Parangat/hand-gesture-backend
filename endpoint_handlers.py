from fastapi import FastAPI, Body
import json



app = FastAPI()

with open('./config/default_config.json', 'r') as file:
    default_config = json.load(file)

with open('./config/user_config.json', 'r') as file:
    user_config = json.load(file)


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
        return {"message": "missing the ststus info in format  {'status': 'current status'}."}, 422

    return {"message": "resetting the internal timer"}


@app.get("/server/config/default")
def get_default_config():
    return default_config

@app.get("/server/config/user")
def get_user_config():
    return user_config

