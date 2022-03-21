import cv2

import camera

camera = camera.Camera()

camera.__int__(53.0, 41.0, 0.74422, 40, 500)

while True:
    frame = camera.update()

    # break on key press
    key = cv2.waitKey(10)
    if key > 0 and key == ord('q'):
        break
