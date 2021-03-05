from tkinter import *
from PIL import Image
from PIL import ImageTk
import cv2
import redis, struct
import numpy as np
from datetime import datetime
import subprocess, os, sys
from  multiprocessing import Process
import capture, preprocess, OCR

root = Tk()
panelA = None
panelB = None

# def fromRedis(r,n):
#      """Retrieve Numpy array from Redis key 'n'"""
#      try:
#         encoded = r.get(n)
#         h, w = struct.unpack('>II',encoded[:8])
#         a = np.frombuffer(encoded, dtype=np.uint8, offset=8).reshape(h,w,3)
#         return a
#      except:
#         pass

# r = redis.Redis(host='localhost', port=6379, db=0)
# try:
#     print(r.ping())
# except:
#     print('could not ping')


image = Image.open('redis_not_started.jpg')
edged = Image.open('redis_not_started.jpg')

def submitCallBack():
    # img = fromRedis(r,'processed_image')
    img = cv2.imread('processed_image.jpg')
    text = moldNo.cget("text")
    now = datetime.now()
    ts = now.strftime("%Y_%m_%d___%H_%M_%S")
    fname = ts + '__mold-' + text + '.png'
    cv2.imwrite( 'log/' + fname,img)
    print(fname)

def show_log():
    path = r'C:\python34\Lib'
    sys.path.append(path)
    cwd = os.getcwd()
    path = os.path.join(cwd,'log')
    FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
    subprocess.run([FILEBROWSER_PATH, path])

def start_redis():
    path = 'C:\\Program Files\\Redis\\redis-server.exe'
    cmd = ['start',path]
    subprocess.call(cmd, shell=True)
    # subprocess.call(path, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True)

# convert the images to PIL format...
image = ImageTk.PhotoImage(image=image)
edged = ImageTk.PhotoImage(image=edged)
# the first panel will store our original image
panelA = Label(image= image)
panelA.image = image
panelA.pack(side="left", padx=10, pady=10)
# while the second panel will store the edge map
ROI_frame = Frame(root)
ROI_frame.pack(side="right", padx=10, pady=10)
panelB = Label(ROI_frame, image= edged)
panelB.image = edged
panelB.pack()
moldNo = Label(ROI_frame, text= 'Hello there')
moldNo.pack()
submit_button = Button ( ROI_frame, text="Submit", command = submitCallBack )
submit_button.pack(fill=X)
root.title("Mold number check")
menubar = Menu(root)
root.config(menu=menubar)
fileMenu = Menu(menubar)
fileMenu.add_command(label="Show Log", command=show_log)
fileMenu.add_command(label="Start Redis Server", command=start_redis)
menubar.add_cascade(label="File", menu=fileMenu)


def update_images():
    # image = fromRedis(r,'rect')
    # edged = fromRedis(r,'processed_image')
    image = cv2.imread('raw.jpg')
    edged = cv2.imread('processed_image.jpg')
    # print(image.shape,image[1][1])
    with open('textout.txt','r') as fin:
        found_digits = fin.readline()
    moldNo.configure(text = found_digits)
    # convert the images to PIL format...
    image = ImageTk.PhotoImage(Image.fromarray(image))
    edged = ImageTk.PhotoImage(Image.fromarray(edged))
    # the first panel will store our original image
    # panelA = Label(image=image)
    # panelA.image = image
    panelA.configure(image=image)
    panelA.image = image
    # while the second panel will store the edge map
    panelB.configure(image=edged)
    panelB.image = edged
    root.after(100, update_images)

root.after(1, update_images)

def startPreprocess():
    prepro = preprocess.Preprocess()
    prepro.run()

def startCapture():
    cap = capture.Capture(1)
    cap.run()

def startOCR():
    ocr = OCR.OCR()
    ocr.run()    

def startGUI():
    root.mainloop()

def main():
    print('starting Capture')
    Process(target=startCapture).start()
    print('starting Preprocess')
    Process(target=startPreprocess).start()
    print('starting OCR')
    Process(target=startOCR).start()
    print('starting GUI')
    Process(target=startGUI).start()

if __name__ == "__main__":
    main()