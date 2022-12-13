import asyncio
import websockets
import cv2
import pickle

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

# create handler for each connection
async def handler(websocket, path):

    frame = cv2.imread('./phil.jpg', cv2.IMREAD_COLOR)
    frameData = cv2.imencode('.jpg', frame, encode_param)[1].tobytes()
 
    data = await websocket.recv()
    reply = f"Data recieved as:  {data}!"
 
    await websocket.send(frameData)

start_server = websockets.serve(handler, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()