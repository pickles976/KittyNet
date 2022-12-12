# https://towardsdatascience.com/image-analysis-for-beginners-creating-a-motion-detector-with-opencv-4ca6faba4b42
import cv2
import numpy as np

def motion_detector(oldFrame, newFrame):

    if oldFrame is None:
        return 0.0

    return np.square(np.subtract(oldFrame, newFrame)).mean()


