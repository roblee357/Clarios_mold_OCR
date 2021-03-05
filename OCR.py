import numpy as np
import cv2
import string
import sys
import os
import pytesseract
from pytesseract import Output
from multiprocessing import Process
from time import sleep
import struct
import redis
import time


class OCR():
    def __init__(self, threshold=None):
        self.DD = self.Del()

    def fromRedis(self, r, n):
        """Retrieve Numpy array from Redis key 'n'"""
        encoded = r.get(n)
        h, w = struct.unpack('>II', encoded[:8])
        a = np.frombuffer(encoded, dtype=np.uint8, offset=8).reshape(h, w, 3)
        return a

    def toRedis(self, r, a, n):
        """Store given Numpy array 'a' in Redis under key 'n'"""
        h, w = a.shape[:2]
        shape = struct.pack('>II', h, w)
        encoded = shape + a.tobytes()

        # Store encoded data in Redis
        r.set(n, encoded)
        return

    class Del:
        def __init__(self, keep=string.digits):
            self.comp = dict((ord(c), c) for c in keep)

        def __getitem__(self, k):
            return self.comp.get(k)

    def run(self):
        # Redis connection
        r = redis.Redis(host='localhost', port=6379, db=0)

        key = 0
        start = time.time()
        while key != 27:
            # img = self.fromRedis(r, 'processed_image')
            img = cv2.imread('processed_image.jpg')
            # print(img.shape)
            try:
                found_text = pytesseract.image_to_string(img, config='--psm 7')
            except:
                found_text = "None"
            found_digits = found_text.translate(self.DD)
            end = time.time()
            print(found_digits, 'elapsed time:', end - start)
            with open('textout.txt', 'w') as fout:
                fout.write(found_digits)
            start = time.time()
            # cv2.imshow('OCR', img)

            # key = cv2.waitKey(1) & 0xFF
            # self.toRedis(r, img, 'OCR_image')
            try:
                cv2.imwrite('OCR_image.jpg',img)
            except Exception as e:
                print(e)



def main():
    ocr = OCR()
    ocr.run()


if __name__ == '__main__':
    main()
