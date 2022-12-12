# https://towardsdatascience.com/image-analysis-for-beginners-creating-a-motion-detector-with-opencv-4ca6faba4b42
import cv2
import numpy as np

def motion_detector(oldFrame, newFrame):

    if oldFrame is None:
        return False

    mse = np.square(np.subtract(oldFrame, newFrame)).mean()

    # threshold for detection ( background noise is less than 2 )
    if mse > 5:
        print("MSE:", mse)
        return True

    return False


