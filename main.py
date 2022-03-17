import cv2
import numpy as np
import sys

import Camera

GOAL_HEIGHT = 105

# Camera params
CAMERA_HEIGHT = 24
CAMERA_ANGLE = 40

# distance between camera and goal
HEIGHT = GOAL_HEIGHT - CAMERA_HEIGHT

VERTICAL_FOV = 41.0
HORIZONTAL_FOV = 53.0

HORIZONTAL_RESOLUTION = 1280
VERTICAL_RESOLUTION = 720


def calc_dist(pix_y: int) -> float:
    """
    Calculate how far a specific pixel is from the camera
    """
    angle = (pix_y / VERTICAL_RESOLUTION) * VERTICAL_FOV - (VERTICAL_FOV / 2)

    return HEIGHT / np.tan(angle)


camera = Camera.Camera()

camera.__int__()

while True:
    frame, binary_img = camera.update()

    contours, hierarchy = cv2.findContours(binary_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, contours, -1, (0, 0, 255))


    for contour in contours:
        if cv2.contourArea(contour) < 15:
            continue

        rect = cv2.minAreaRect(contour)
        center, size, angle = rect
        center = tuple([int(dim) for dim in center])

        cv2.circle(frame, center, 3, (0, 0, 255), -1)


    cv2.imshow("Video Capture", frame)

    # break on key press
    key = cv2.waitKey(10)
    if key > 0 and key == 255:
        break
