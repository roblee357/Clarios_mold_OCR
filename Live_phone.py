import os
import pathlib
import cv2
from threading import Thread, Event

class Live_phone:
    def __init__(self):
        self.img = None
    def get(self, img):
        # self.img = img
        i = 0
        while True:
            try:
                path = 'Android_Web\\flask\\examples\\tutorial\\flaskr\\images\\live.png'
                self.img = cv2.imread(path)
                # os.remove(path)
            except Exception as e:
                i =+ 1
                # print(e , i)

    def start_getting(self):
        t = Thread(target=self.get, args=(self.img, ))
        t.start()
   

def main():
    lv = Live_phone()
    lv.start_getting()
    while True:
        try:
            cv2.imshow('this',lv.img)
            cv2.waitKey(1)
        except:
            pass

    # lv.live()

if __name__ == '__main__':
    main()
