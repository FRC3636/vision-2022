import sys

import cv2


def green_filter(img):
    filtered_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    filtered_img = cv2.GaussianBlur(filtered_img, (5, 5), 0)
    filtered_img = cv2.inRange(filtered_img, (60, 25, 100), (90, 255, 255), filtered_img)
    return filtered_img


class Camera:

    __cam = 0

    def __int__(self):
        cv2.namedWindow("Video Capture", cv2.WINDOW_AUTOSIZE)

        print("done")

        self.__cam = cv2.VideoCapture(0)  # 0 is the default camera

        self.__cam.set(15, 1)

        if not self.__cam.isOpened():
            print("unable to open default camera")
            sys.exit(1)

    def update(self):
        ret, frame = self.__cam.read()
        if frame.shape[0] > 0:
            binary_img = green_filter(frame)
            cv2.imshow("Binary Image", binary_img)
            return frame, binary_img
