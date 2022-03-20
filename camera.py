import sys

import cv2
import numpy as np

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

    __goal_height = 2.643

    # Camera params
    __camera_height = 0
    __camera_angle = 0
    __horizontal_fov = 0
    __vertical_fov = 0
    __horizontal_resolution = 0
    __vertical_resolution = 0

    # distance between camera and goal
    __relative_height = 0

    def __int__(self, horizontal_fov, vertical_fov, camera_height, camera_angle):

        self.__horizontal_fov = horizontal_fov
        self.__vertical_fov = vertical_fov
        self.__camera_height = camera_height
        self.__camera_angle = camera_angle

        self.__relative_height = self.__goal_height - self.__camera_height

        cv2.namedWindow("Video Capture")

        self.__cam = cv2.VideoCapture(0)  # 0 is the default camera

        if not self.__cam.isOpened():
            print("unable to open default camera")
            sys.exit(1)

        ret, frame = self.__cam.read()

        self.__horizontal_resolution = frame.shape[0]
        self.__vertical_resolution = frame.shape[1]

        # Used for tuning HSV threshold
        cv2.createTrackbar("H Lower", "Video Capture", 0, 180, hl)
        cv2.createTrackbar("S Lower", "Video Capture", 0, 255, sl)
        cv2.createTrackbar("V Lower", "Video Capture", 0, 255, vl)
        cv2.createTrackbar("H Upper", "Video Capture", 0, 180, hh)
        cv2.createTrackbar("S Upper", "Video Capture", 0, 255, sh)
        cv2.createTrackbar("V Upper", "Video Capture", 0, 255, vh)

    def calc_dist(self, pix_y: int) -> float:
        """
        Calculatfix e how far a target it from the camera
        """
        angle = (pix_y / self.__vertical_resolution) * self.__vertical_fov - (self.__vertical_fov / 2)

        return self.__relative_height / np.tan(angle)

    def calc_angle(self, pix_x: int) -> float:
        angle = (pix_x / self.__horizontal_resolution) * self.__horizontal_fov - (self.__horizontal_fov / 2)

        return angle

    def update(self):
        ret, frame = self.__cam.read()
        if frame.shape[0] > 0:
            binary_img = green_filter(frame)
            cv2.imshow("Binary Image", binary_img)

            cv2.imshow("Video Capture", frame)

            # Get each individual shape
            contours, hierarchy = cv2.findContours(binary_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(frame, contours, -1, (0, 0, 255))

            # best_contour = contours[0]

            for contour in contours:
                if cv2.contourArea(contour) < 15:
                    continue

                rect = cv2.minAreaRect(contour)
                center, size, angle = rect
                center = tuple([int(dim) for dim in center])

                cv2.circle(frame, center, 3, (0, 0, 255), -1)

            return frame
