import numpy as np
import cv2, string, sys, os, json, time
import pytesseract
from pytesseract import Output
from  multiprocessing import Process
from time import sleep
import struct
import argparse
import pickle as pkl
from threading import Thread
import capture

configPath = 'config.json'

class Processor():
    def __init__(self):
        pass

    def run(self, img):
        # ii = 0
        while True:
            img = self.capture.img
            # print('looping like cra cra', ii)
            # ii += 1
            try:
                with open(configPath,'rb') as fin:
                    config = json.load(fin)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img = cv2.medianBlur(img,5)
                threshold = None
                if not threshold is None:
                    img = eval ('cv2.threshold(img,0,255,' + threshold +' )[1]' ) # cv2.THRESH_BINARY + cv2.THRESH_OTSU
                img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
                img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                scale_percent = 100 #config['scale_percent']
                img_w = int(img.shape[1] * scale_percent / 100)
                img_h = int(img.shape[0] * scale_percent / 100)
                h_padding_factor = config['crop_h_padding_factor']
                v_padding_factor = config['crop_v_padding_factor']
                h_padding = int(h_padding_factor * scale_percent / 100)
                v_padding = int(v_padding_factor * scale_percent / 100)
                dsize = (img_w, img_h)
                img = cv2.resize(img, dsize)
                crop_img = img[ v_padding:img_h-v_padding, h_padding:img_w-h_padding]
                scale_percent = 100
                crop_w = crop_img.shape[1]
                crop_h = crop_img.shape[0]
                rect_img_w = int(crop_w * scale_percent / 100)
                rect_img_h = int(crop_h * scale_percent / 100)
                rect_h_padding_factor = config['rect_h_padding_factor']
                rect_v_padding_factor = config['rect_v_padding_factor']
                rect_h_padding = int(rect_img_w * rect_h_padding_factor / 100)
                rect_v_padding = int(rect_img_h * rect_v_padding_factor / 100)
                crop_img = cv2.rectangle(crop_img,(rect_h_padding,rect_v_padding),(crop_w-rect_h_padding,crop_h-rect_v_padding),(255,0,0),3)
                self.rect = crop_img
                cv2.imwrite('rect.jpg',crop_img)
                ROI = crop_img[rect_v_padding:crop_h-rect_v_padding,rect_h_padding:crop_w-rect_h_padding]
                scale_percent = config['scale_percent']
                ROI_w = int(ROI.shape[1] * scale_percent / 100)
                ROI_h = int(ROI.shape[0] * scale_percent / 100)
                dsize = (ROI_w, ROI_h)
                ROI = cv2.resize(ROI, dsize)
                self.img = ROI

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                print(e)

    def start(self,capture):
        self.capture = capture
        self.img = None
        t = Thread(target=self.run, args=(self.img, ))
        t.start()          

def main():
    cap = capture.Capture(0)
    print('before run')
    cap.start()
    t = time.time()
    while cap.img is None:
        print('waiting for camera to connect',time.time()-t)
        time.sleep(.25)

    proc = Processor()
    proc.start(cap)

    while proc.img is None:
        print('waiting for processed image',time.time()-t)
        time.sleep(.25)
    ii = 0
    while True:
        processed = proc.img
        print(processed.shape, ii)
        ii += 1
        cv2.imshow('this',processed)    
        cv2.waitKey(1)

if __name__ == '__main__':
    main()
