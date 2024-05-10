import asyncio
import websockets
import datetime

state = {"ws_state": "run"}

async def time_server(websocket):
    while True:
        if state["ws_state"] == "run":
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await websocket.send(current_time)
            await asyncio.sleep(0.2)
        else:
            break

start_server = websockets.serve(time_server, "localhost", 8001)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
