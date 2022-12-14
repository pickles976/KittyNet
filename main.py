import cv2
import time
import motion_detection
import os
import sys
import argparse
from datetime import datetime

FPS = 1.0
PATH = 'images'
COLD_START = 30
os.chdir(PATH)

def start_capture(save_images=False, show_webcam=False, denoise=True, threshold=10.0):

    print(f"--save-images {save_images}, --show-webcam {show_webcam}")

    print("Initializing webcam...")
    imgCap = cv2.VideoCapture(0)

    time_elapsed = 0
    prev = 0
    oldFrame = None
    frameNum = 0

    print("Webcam cold start...")
    while True:

        time_elapsed = time.time() - prev

        if time_elapsed > 1.0/30.0:

            if frameNum < COLD_START:
                # Capture the video frame
                ret, frame = imgCap.read()
                frameNum += 1
            else:
                frameNum = 0
                break

    print("Webcam initialized!")

    while True:

        time_elapsed = time.time() - prev

        if time_elapsed > 1.0/FPS:

            # Capture the video frame
            ret, frame = imgCap.read()

            prepared_frame = frame

            # cleanup
            # prepared_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # gray 
            # prepared_frame = cv2.resize(prepared_frame, (256, 256)) # resize

            # # denoising can be an expensive operation
            if denoise:
                prepared_frame = cv2.GaussianBlur(src=prepared_frame, ksize=(5,5), sigmaX=0) # denoise

            mse = motion_detection.motion_detector(oldFrame, prepared_frame) # get mean squared error
            print(f"MSE: {mse:.2f}")

            # detect motion and save image
            if save_images and mse > threshold:

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # save image with mean-squared error data
                print(f"Saving image with MSE: {mse:.2f}")
                cv2.imwrite(f"{timestamp}_{mse:.0f}.jpg", frame)
                frameNum += 1

            oldFrame = prepared_frame
        
            # Display the resulting frame
            if show_webcam: cv2.imshow('frame', frame)
            
            # q to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            prev = time.time()

    # After the loop release the cap object
    imgCap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

def read_cmdline():
    p=argparse.ArgumentParser()
    p.add_argument('function') 
    p.add_argument("--save-images", type=str,required=False)
    p.add_argument("--show-webcam", type=str, required=False)
    p.add_argument("--denoise", type=str, required=False)
    p.add_argument("--threshold",type=float, required=False, default=10.0)
    args=p.parse_args()
    return args 

if __name__ == '__main__':
    args = read_cmdline()
    print(args)
    globals()[args.function](args.save_images.lower()=="true", args.show_webcam.lower()=="true", args.denoise.lower()=="true", args.threshold)

