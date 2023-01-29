# echo-server.py
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time
import asyncio
import websockets

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
SCALE = 0.7
FPS = 1.0

print("Initializing webcam...")
camera = PiCamera()
rawCapture = PiRGBArray(camera)
print("Webcam initialized!")

# create handler for each connection
async def handler(websocket, path):

    time_elapsed = 0
    prev = 0

    while True:

        time_elapsed = time.time() - prev

        if time_elapsed > 1.0/FPS:

            # Capture the video frame
            camera.capture(rawCapture, format="bgr")
            frame = rawCapture.array

            # Resize
            width = int(frame.shape[1] * SCALE)
            height = int(frame.shape[0] * SCALE)
            frame = cv2.resize(frame, (width, height))

            # To bytes
            frameData = cv2.imencode('.jpg', frame, encode_param)[1].tobytes()
        
            await websocket.send(frameData)

            prev = time.time()

print("Starting server thread...")
start_server = websockets.serve(handler, "", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()