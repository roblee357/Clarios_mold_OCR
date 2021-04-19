import cv2, time, json
import struct
##import redis
import numpy as np
import ctypes
import argparse
from random import randrange
import pickle as pkl
# from multiprocessing import Process, Value, Array
from threading import Thread, Event

def parseCmdLineArgs ():
    # parse the command line
    parser = argparse.ArgumentParser ()
    # add optional argument to turn off the broker
    parser.add_argument ("-v","--verbosity",default='', help="Be Verbose")
    # parse the args
    args = parser.parse_args ()
    return args

class Capture():

    def __init__(self, camera):
        self.camera = camera
        self.img = None
        print('starting Capture')
        # multiprocessing.Process(target=self.run).start()

    # def toRedis(self,r,a,n):
    #     """Store given Numpy array 'a' in Redis under key 'n'"""
    #     h, w = a.shape[:2]
    #     shape = struct.pack('>II',h,w)
    #     encoded = shape + a.tobytes()
    #     # Store encoded data in Redis
    #     r.set(n,encoded)
    #     return

    # def toZMQ(self,a, arrayname="NoName",flags=0, copy=True, track=False):
    #     # self.zmq.imshow("Raw capture", a)
    #     md = dict(
    #         arrayname = arrayname,
    #         dtype = str(a.dtype),
    #         shape = a.shape,
    #         data = a.tolist()
    #     )
    #     print( 'sending', md['dtype'])
    #     self.socket.send_string("raw %s" % (json.dumps(md)))
    #     # self.socket.send_string('hello') #_json(md, 0)  #flags|zmq.SNDMORE)
    #     # return self.socket.send(a, flags, copy=copy, track=track)

    def run(self,img):
        # Redis connection
        self.img = img
##        r = redis.Redis(host='localhost', port=6379, db=0)
        cam = cv2.VideoCapture(self.camera)
        key = 0
        while key != 27:
            try:
                ret, self.img = cam.read()
                self.img = cv2.cvtColor(self.img,cv2.COLOR_BGR2RGB)
            except Exception as e:
                cam = cv2.VideoCapture(self.camera)
                print('reconnecting 2',e)  
    def start(self):
        self.img = None
        t = Thread(target=self.run, args=(self.img, ))
        t.start()

def main():
    args = parseCmdLineArgs ()
    cap = Capture(0)
    print('before run')
    cap.start()
    t = time.time()
    while cap.img is None:
        print('waiting for camera to connect',time.time()-t)
        time.sleep(.25)

    # t = time.time()
    while True:
        cv2.imshow('this',cap.img)
        cv2.waitKey(1)
        # print('Running',time.time()-t)
        # t = time.time()

if __name__ == '__main__':
    main()
