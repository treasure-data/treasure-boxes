import time

import numpy as np

import cv2
import imutils
import scorer
from imutils.object_detection import non_max_suppression


class PedestrianDetector:
    def __init__(self):
        self.cap = scorer.VideoCapture(0)
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def detect(self):
        vframe = None
        while vframe is None:
            vframe = self.cap.read()

        image = vframe.get_bgr()

        # Reference: https://www.pyimagesearch.com/2015/11/09/pedestrian-detection-opencv/

        # resize for (1) reducting run time, (2) improving accuracy
        imutils.resize(image, width=min(400, image.shape[1]))
        (rects, weights) = self.hog.detectMultiScale(
            image, winStride=(4, 4), padding=(8, 8), scale=1.05
        )

        # apply non-maxima suppression to the bounding boxes
        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

        for (xA, yA, xB, yB) in pick:
            cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)

        scorer.imshow(1, image)

        return len(pick), int(time.mktime(vframe.datetime.timetuple()))
