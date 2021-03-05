import numpy as np
import cv2
import zmqimage
print("Connecting to zmqShowImage Server ... ")
zmq = zmqimage.zmqConnect(connect_to="tcp://127.0.0.1:5555")
for i in range(255):
    image = np.ones((500, 500), dtype="uint8")*i
    zmq.imshow("Zero Image 500 x 500", image)
    # build a rectangular mask & display it
    mask = np.zeros(image.shape[:2], dtype="uint8")
    cv2.rectangle(mask, (0, 90), (300, 450), 255, -1)
    zmq.imshow("Rectangular Mask", mask)