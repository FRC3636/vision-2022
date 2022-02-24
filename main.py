import cv2
from numpy import tan
import sys

GOAL_HEIGHT = 105

# Camera params
CAMERA_HEIGHT = 24
CAMERA_ANGLE = 45

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

    return HEIGHT / tan(angle)


def green_filter(frame) -> None:
    newframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    newframe = cv2.GaussianBlur(newframe, (5, 5), 0)
    newframe = cv2.inRange(newframe, (60, 25, 100), (90, 255, 255), newframe)
    return newframe


cv2.namedWindow("Video Capture", cv2.WINDOW_AUTOSIZE)

cam = cv2.VideoCapture(0)  # 0 is the default camera

if not cam.isOpened():
    print("unable to open default camera")
    sys.exit(1)

while True:
    ret, frame = cam.read()
    if frame.shape[0] > 0:
        frame = green_filter(frame)
        cv2.imshow("Video Capture", frame)

    # break on key press
    key = cv2.waitKey(10)
    if key > 0 and key != 255:
        break
