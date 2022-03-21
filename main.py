import cv2

import camera
import network

camera = camera.Camera()
# nt = network.Network()

camera.__int__(53.0, 41.0, 0.74422, 40, 500)
# nt.__init__()

while True:
    frame, dist, angle = camera.update()

    # nt.update(dist, angle)

    # break on key press
    key = cv2.waitKey(10)
    if key > 0 and key == ord('q'):
        break
