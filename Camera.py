import sys

import cv2

range_lower = [60, 25, 100]
range_upper = [90, 255, 255]


def hl(value):
    range_lower[0] = value


def sl(value):
    range_lower[1] = value


def vl(value):
    range_lower[2] = value


def hh(value):
    range_upper[0] = value


def sh(value):
    range_upper[1] = value


def vh(value):
    range_upper[2] = value


def green_filter(img):
    filtered_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    filtered_img = cv2.GaussianBlur(filtered_img, (5, 5), 0)
    filtered_img = cv2.inRange(filtered_img, tuple(range_lower), tuple(range_upper), filtered_img)
    return filtered_img


class Camera:
    __cam = 0

    def __int__(self):
        cv2.namedWindow("Video Capture")

        self.__cam = cv2.VideoCapture(0)  # 0 is the default camera

        if not self.__cam.isOpened():
            print("unable to open default camera")
            sys.exit(1)

        # Used for tuning HSV threshold
        cv2.createTrackbar("H Lower", "Video Capture", 0, 180, hl)
        cv2.createTrackbar("S Lower", "Video Capture", 0, 255, sl)
        cv2.createTrackbar("V Lower", "Video Capture", 0, 255, vl)
        cv2.createTrackbar("H Upper", "Video Capture", 0, 180, hh)
        cv2.createTrackbar("S Upper", "Video Capture", 0, 255, sh)
        cv2.createTrackbar("V Upper", "Video Capture", 0, 255, vh)

    def update(self):
        ret, frame = self.__cam.read()
        if frame.shape[0] > 0:
            binary_img = green_filter(frame)
            cv2.imshow("Binary Image", binary_img)
            return frame, binary_img
