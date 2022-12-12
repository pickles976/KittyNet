import cv2
import time
import motion_detection
import os
import sys
import argparse

PATH = 'images'
os.chdir(PATH)

def start_capture(save_images=False, show_webcam=False):

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
            if motion_detection.motion_detector(oldFrame, prepared_frame) and save_images:
                cv2.imwrite(f"{frameNum}.jpg", prepared_frame)
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
    p.add_argument("--save-images",type=bool, choices=[True,False],required=False)
    p.add_argument("--show-webcam",type=bool, choices=[True,False],required=False)
    args=p.parse_args()
    return args 

if __name__ == '__main__':
    args = read_cmdline()
    print(args)
    globals()[args.function](args.save_images, args.show_webcam)

