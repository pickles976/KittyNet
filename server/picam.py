import asyncio
import websockets
import cv2
import time

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
SCALE = 0.7
FPS = 24.0

print("Initializing webcam...")
imgCap = cv2.VideoCapture(0)
print("Webcam initialized!")

# create handler for each connection
async def handler(websocket, path):

    while True:

        # Capture the video frame
        ret, frame = imgCap.read()

        # Resize
        width = int(frame.shape[1] * SCALE)
        height = int(frame.shape[0] * SCALE)
        frame = cv2.resize(frame, (width, height))

        # To bytes
        frameData = cv2.imencode('.jpg', frame, encode_param)[1].tobytes()
    
        await websocket.send(frameData)

print("Starting server thread...")
start_server = websockets.serve(handler, "", 8000)
print("Ready to accept connections...")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()