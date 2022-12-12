import cv2
import time
import motion_detection
import os

PATH = 'images'
os.chdir(PATH)

print("Initializing webcam...")
imgCap = cv2.VideoCapture(0)
print("Webcam initialized!")

FPS = 0.3

time_elapsed = 0
prev = 0
oldFrame = None
frameNum = 0

while True:

    time_elapsed = time.time() - prev

    if time_elapsed > 1.0/FPS:

        # Capture the video frame
        ret, frame = imgCap.read()

        # cleanup
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # gray 
        resized_frame = cv2.resize(gray_frame, (256, 256)) # resize
        prepared_frame = cv2.GaussianBlur(src=resized_frame, ksize=(5,5), sigmaX=0) # denoise

        # detect motion and save image
        if motion_detection.motion_detector(oldFrame, prepared_frame):
            cv2.imwrite(f"{frameNum}.jpg", prepared_frame)
            frameNum += 1

        oldFrame = prepared_frame
    
        # Display the resulting frame
        cv2.imshow('frame', frame)
        
        # q to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        prev = time.time()


# After the loop release the cap object
imgCap.release()
# Destroy all the windows
cv2.destroyAllWindows()
