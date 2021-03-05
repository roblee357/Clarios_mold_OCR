import numpy as np
import cv2, string, sys, os, json
import pytesseract
from pytesseract import Output
from  multiprocessing import Process
from time import sleep
import struct
import redis, argparse, zmq
import pickle as pkl

class Preprocess():
    def __init__(self,threshold=None):
        self.threshold = threshold
        self.configPath = 'config.json'
        with open(self.configPath,'r') as fin:
            self.config = json.load(fin)
        # self.zmq_get_raw = zmqimage.zmqImageShowServer(open_port="tcp://*:5555")
        #  Socket to talk to server
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect("tcp://localhost:5555")
        print('connected to tcp://localhost:5555')


    def recv_array(self, flags=0, copy=True, track=False):
        """recv a numpy array, including arrayname, dtype and shape"""
        md = self.socket.recv_json(flags=flags)
        print('recieved json')
        msg = self.socket.recv(flags=flags, copy=copy, track=track)
        A = np.frombuffer(msg, dtype=md['dtype'])
        return  (md['arrayname'], A.reshape(md['shape']))

    def fromRedis(self,r,n):
        """Retrieve Numpy array from Redis key 'n'"""
        encoded = r.get(n)
        h, w = struct.unpack('>II',encoded[:8])
        a = np.frombuffer(encoded, dtype=np.uint8, offset=8).reshape(h,w,3)
        return a

    # def toRedis(self,r,a,n):
    #     """Store given Numpy array 'a' in Redis under key 'n'"""
    #     h, w = a.shape[:2]
    #     shape = struct.pack('>II',h,w)
    #     encoded = shape + a.tobytes()
    #     # Store encoded data in Redis
    #     r.set(n,encoded)
    #     return

    def run(self):
        # cap = cv2.VideoCapture(1)
            # Redis connection
        r = redis.Redis(host='localhost', port=6379, db=0)
        key = 0

        while(True):
            try:
                with open(self.configPath,'rb') as fin:
                    self.config = json.load(fin)
                # Capture frame-by-frame
                # ret, frame = cap.read()
                frame = self.fromRedis(r,'image')
                # arrayname, frame = self.zmq_get_raw.getArray()
                # frame = cv2.imread('raw.jpg')
                # with open('raw.pkl','rb') as f:
                #     frame = pkl.load(f)
                #     print(frame.shape)
                # frame = self.recv_array()
                # print('frame',frame)
                # with open('raw.out','rb') as fin:
                #     frame = np.load(fin)
                # frame = frame.reshape(frame.shape[0], frame.shape[1] // 3, 3) 
                # Our operations on the frame come here
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                img = cv2.medianBlur(img,5)
                if not self.threshold is None:
                    img = eval ('cv2.threshold(img,0,255,' + self.threshold +' )[1]' ) # cv2.THRESH_BINARY + cv2.THRESH_OTSU
                img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
        
                #percent by which the image is resized
                scale_percent = 100 #config['scale_percent']

                #calculate the 50 percent of original dimensions
                img_w = int(img.shape[1] * scale_percent / 100)
                img_h = int(img.shape[0] * scale_percent / 100)
                h_padding_factor = self.config['crop_h_padding_factor']
                v_padding_factor = self.config['crop_v_padding_factor']
                h_padding = int(h_padding_factor * scale_percent / 100)
                v_padding = int(v_padding_factor * scale_percent / 100)

                # dsize
                dsize = (img_w, img_h)

                # resize image
                img = cv2.resize(img, dsize)

                crop_img = img[ v_padding:img_h-v_padding, h_padding:img_w-h_padding]
                scale_percent = 100
                crop_w = crop_img.shape[1]
                crop_h = crop_img.shape[0]
                rect_img_w = int(crop_w * scale_percent / 100)
                rect_img_h = int(crop_h * scale_percent / 100)
                rect_h_padding_factor = self.config['rect_h_padding_factor']
                rect_v_padding_factor = self.config['rect_v_padding_factor']
                rect_h_padding = int(rect_img_w * rect_h_padding_factor / 100)
                rect_v_padding = int(rect_img_h * rect_v_padding_factor / 100)

                crop_img = cv2.rectangle(crop_img,(rect_h_padding,rect_v_padding),(crop_w-rect_h_padding,crop_h-rect_v_padding),(255,0,0),3)
                # print('v_padding',v_padding,'h_padding',h_padding,'img_h-v_padding',img_h-v_padding,'img_w-h_padding',img_w-h_padding,'img shape',img.shape)
                # self.toRedis(r, crop_img, 'rect')
                cv2.imwrite('rect.jpg',crop_img)
                # cv2.imshow('Preprocessed',crop_img)
                ROI = crop_img[rect_v_padding:crop_h-rect_v_padding,rect_h_padding:crop_w-rect_h_padding]
                #percent by which the image is resized
                scale_percent = self.config['scale_percent']

                #calculate the 50 percent of original dimensions
                ROI_w = int(ROI.shape[1] * scale_percent / 100)
                ROI_h = int(ROI.shape[0] * scale_percent / 100)

                # dsize
                dsize = (ROI_w, ROI_h)

                # resize image
                ROI = cv2.resize(ROI, dsize)

                # self.toRedis(r, ROI, 'processed_image')
                cv2.imwrite('processed_image.jpg',ROI)
                sleep(0.01)
                cv2.imshow('raw image',frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                print(e)

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

def main():
    preprocess = Preprocess()
    preprocess.run()

if __name__ == "__main__":
    main()