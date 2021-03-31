import numpy as np
import cv2
import string
import sys
import os
import pytesseract
from pytesseract import Output
from threading import Thread, Event
from time import sleep
import struct
# import redis
import time
import preprocess

class OCR():
    def __init__(self, threshold=None):
        self.DD = self.Del()

    class Del:
        def __init__(self, keep=string.digits):
            self.comp = dict((ord(c), c) for c in keep)

        def __getitem__(self, k):
            return self.comp.get(k)

    def run(self, txt):
        # Redis connection
        # r = redis.Redis(host='localhost', port=6379, db=0)
        self.txt = txt
        key = 0
        start = time.time()
        while key != 27:
            # img = self.fromRedis(r, 'processed_image')
            # img = cv2.imread('processed_image.jpg')
            img = self.pro_img.img
            # print(img.shape)
            try:
                found_text = pytesseract.image_to_string(img, config='--psm 7')
            except:
                found_text = "None"
            found_digits = found_text.translate(self.DD)
            end = time.time()
            print(found_digits, 'elapsed time:', end - start)
            self.txt = found_digits
            with open('textout.txt', 'w') as fout:
                fout.write(found_digits)
            start = time.time()
            try:
                cv2.imwrite('OCR_image.jpg',img)
            except Exception as e:
                print(e)
    
    def start(self, pro_img):
        self.pro_img = pro_img
        # processedimage = preprocess.process(capture.img)
        self.txt = None
        t = Thread(target=self.run, args=(self.txt, ))
        t.start()        



def main():
    ocr = OCR()
    ocr.run()


if __name__ == '__main__':
    main()
