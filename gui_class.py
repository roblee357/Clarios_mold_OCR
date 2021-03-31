from tkinter import *
import PIL.Image
import PIL.ImageTk
import cv2, time
import numpy as np
from datetime import datetime
import subprocess, os, sys
from threading import Thread
import capture, preprocess, OCR, win_loc, badges
from Live_phone import Live_phone
import pyautogui,  keyboard, json, win32clipboard
from tkinter import *
import ctypes

class Camera:

    def __init__(self, cam_no):
        self.root = Tk()
        self.cam_no = cam_no
        self.setupCameraGUI()
        self.setupMoldButton()
        self.root.withdraw()
        self.badge = badges.Badge(master = self.root)
        # self.readBadges()

    def setupMoldButton(self):
        self.configPath = 'config.json'
        with open(self.configPath,'r') as fin:
            self.config = json.load(fin)
        try:
            self.bs_pos = win_loc.main()
        except:
            ctypes.windll.user32.MessageBoxW(0, "Please start PSMII Bluesheet", "Error", 0)
        self.right_pos = self.bs_pos[0] + self.bs_pos[2] - self.config["win_width"] -20
        self.down_pos = self.bs_pos[1] + 265
        self.win_width = self.config["win_width"]
        self.win_height = self.config["win_height"] 
        self.win_width_s = str(self.win_width) + 'x'
        self.win_height_s = str(self.win_height) + '+'
        self.right_pos_s = str(self.right_pos) + '+'
        self.down_pos_s = str(self.down_pos)
        self.moldButtonWindow = Toplevel(self.root)
        self.moldButtonWindow.configure(bg='blue')
        self.moldButtonWindow.overrideredirect(1)
        self.moldButtonWindow.geometry(self.win_width_s + self.win_height_s + self.right_pos_s + self.down_pos_s)
        self.moldButtonWindow.attributes('-alpha', 0.3)
        self.moldButtonWindow.lift()
        self.moldButtonWindow.attributes('-topmost', True)
        self.moldButtonWindow.btn = Button(self.moldButtonWindow,  
                    text ="",  # Hardest button to button
                    command = self.showInstructionWindow,
                    background='blue') 
        self.moldButtonWindow.btn.pack(fill=BOTH, expand=1) 
        # self.moldButtonWindow.

    def showInstructionWindow(self):
        print('clicked')
        self.instructionWindow = Toplevel(self.root,takefocus=True)
        self.moldButtonWindow.withdraw()
        self.instruction_image = PIL.Image.open('Capture_Instruction.PNG')
        self.instruction_image = PIL.ImageTk.PhotoImage(image=self.instruction_image)
        self.instructionWindowPanel = Label(master = self.instructionWindow, image= self.instruction_image)
        self.instructionWindowPanel.image = self.ROI
        self.instructionWindowPanel.pack()
        self.instructionWindow.after(1000, self.checkForNewImg)


    def checkForNewImg(sef):
        print('checking for new image')

    def showCameraWindow(self):
        print('clicked')
        # self.root.deiconify()
        self.m = 0
        self.showWindow(self.root)
        self.moldButtonWindow.withdraw()



    def setupCameraGUI(self):
        self.panelA = None
        self.panelB = None
        self.image = PIL.Image.open('redis_not_started.jpg')
        self.ROI = PIL.Image.open('redis_not_started.jpg')
        # convert the images to PIL format...
        self.image = PIL.ImageTk.PhotoImage(image=self.image)
        self.ROI = PIL.ImageTk.PhotoImage(image=self.ROI)
        # the first panel will store our original image
        self.panelA = Label(image= self.image)
        self.panelA.image = self.image
        self.panelA.pack(side="left", padx=10, pady=10)
        # while the second panel will store the edge map
        self.ROI_frame = Frame( self.root)
        self.ROI_frame.pack(side="right", padx=10, pady=10)
        self.root.title("Mold number check.   Press any key to accept.")
        self.root.focus_force()
        self.root.bind('<KeyPress>', self.key_down_event)
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Show Log", command=self.show_log)
        # fileMenu.add_command(label="Start Redis Server", command=start_redis)
        menubar.add_cascade(label="File", menu=fileMenu)
        self.m = 0
        # self.root.after(1, self.update_images)

    def key_down_event(self,e):
        if self.m == 0:
            print('Down\n', e.char, '\n', e)
            self.m = 1
            self.root.withdraw()
            self.setupConfirmationWindow()

    def setupConfirmationWindow(self):
        self.confWindow = Toplevel(self.root,takefocus=True)
        self.confWindow.focus()
        self.confWindow.grab_set()  #for disable main window
        self.confWindow.attributes('-topmost',True)  #for focus on toplevel
        self.confWindow.focus_force()
        self.confWindow.title("Confirm mold number.")
        self.confWindowPanel = Label(master = self.confWindow, image= self.ROI)
        self.confWindowPanel.image = self.ROI
        self.confWindowPanel.pack()
        default_text = "Mold No."  if len(self.ocr.txt)==0 else self.ocr.txt
        self.moldNoText = StringVar(self.confWindow, value=default_text)
        print('StringVar self.moldNoText',self.moldNoText)
        self.moldNo = Entry(self.confWindow, textvariable = self.moldNoText, font = "Helvetica 44 bold")
        self.moldNo.pack()
        self.confWindow.after(1000, self.sendTab)
        self.confWindow.bind('<Return>', self.confWindow_accept) 

    def confWindow_accept(self, e ):
        self.confWindow.withdraw()
        print('mold no confirmed Down\n', e.char, '\n', e)
        self.root.withdraw()
        # time.sleep(.02)
        # print('really?? this is a non-iterable? Check again bubs.',self.badge.scan())
        self.badge.scan()
        self.operatorFirstName, self.operatorLastName = self.badge.lookedUpName
        self.enter_mold_no_to_bluesheet()
        self.moldButtonWindow.deiconify() 

    def sendTab(self):
        pyautogui.press('tab')
        print('sent tab')

    def enter_mold_no_to_bluesheet(self):
        self.moldButtonWindow.withdraw()
        print('withdrawn mold button')
        # time.sleep(5)
        self.click_x = self.right_pos + round(0.5 * self.win_width)
        self.click_y = self.down_pos + round(0.5 * self.win_height)
        pyautogui.click(x=self.click_x,y=self.click_y,clicks=1)
        self.moldNoText = self.moldNo.get()
        pyautogui.write(self.moldNoText) 
        self.showWindow(self.moldButtonWindow)

    def showWindow(self,window):
        window.deiconify()
        window.lift()
        window.focus()
        window.focus_force()
        window.grab_set()
        window.grab_release()        



    def submitCallBack(self):
        # img = fromRedis(r,'processed_image')
        self.img = cv2.imread('processed_image.jpg')
        # img = panelB.image
        self.text = self.moldNo.cget("text")
        self.now = datetime.now()
        self.ts = self.now.strftime("%Y_%m_%d___%H_%M_%S")
        self.fname = self.ts + '__mold-' + self.text + '.png'
        cv2.imwrite( 'log/' + self.fname,self.root.proc.img)
        print(self.fname)
        self.root.withdraw()
        self.confWindow.withdraw()
        self.m = 0
        self.moldButtonWindow.deiconify()

    def show_log(self):
        self.path = r'C:\python34\Lib'
        sys.path.append(self.path)
        self.cwd = os.getcwd()
        self.path = os.path.join(self.cwd,'log')
        self.FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
        subprocess.run([self.FILEBROWSER_PATH, self.path])

    def update_images(self):
        result = None
        # while result is None:
            # try:
            #     print('updatine images...........................')
            #     self.image = self.root.lv.img # self.root.proc.rect # cv2.imread('\\Android_Web\\flask\\examples\\tutorial\\flaskr\\images\\live.png') #  cap.img #
            #     cv2.imshow('this',self.image)
            #     cv2.waitKey(1)
            #     result = "success"
            # except Exception as e:
            #     print('update images error',e)
        # self.ROI = self.root.proc.img #cv2.imread('processed_image.jpg')
        # with open('textout.txt','r') as fin:
        #     found_digits = fin.readline()
        # newsize = (1200,800)
        # self.image = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(self.image).resize(newsize))
        
        self.ROI = self.image # PIL.ImageTk.PhotoImage(PIL.Image.fromarray(self.ROI))
        self.panelA.configure(image=self.image)
        self.panelA.image = self.image
        self.root.after(100, self.update_images)

    def startPreprocess(self):
        self.prepro = preprocess.Preprocess()
        self.prepro.run()

    def startCapture(self):
        self.cap = capture.Capture(1)
        self.cap.run()

    def startOCR(self):
        self.ocr = OCR.OCR()
        self.ocr.run()    

    def startGUI(self):
        # self.cap = capture.Capture(self.cam_no)
        # print('before run')
        # self.cap.start()
        # self.t = time.time()
        # while self.cap.img is None:
        #     print('waiting for camera to connect',time.time()-self.t)
        #     time.sleep(.25)
        # self.proc = preprocess.Processor()
        # self.proc.start(self.cap)
        # while self.proc.img is None:
        #     print('waiting for processed image',time.time()-self.t)
        #     time.sleep(.25)

        # self.ocr = OCR.OCR()
        # self.ocr.start(self.proc)
        # while self.ocr.txt is None:
        #     print('waiting for OCR',time.time()-self.t)
        #     time.sleep(.25)

        # self.lv = Live_phone()
        # self.lv.start_getting()
        # while self.lv.img is None:
        #     print('waiting for Live phone image',time.time()-self.t)
        #     time.sleep(.25)


        # self.root.cap = self.cap
        # self.root.proc = self.proc
        # self.root.lv = self.lv
        # while True:
        #     try:
        #         cv2.imshow('this',self.root.lv.img)
        #         cv2.waitKey(1)
        #     except:
        #         pass
        self.root.mainloop()


def main():
    cam_no = 1
    cam = Camera(1)
    cam.startGUI()
    print('after GUI start')

if __name__ == "__main__":
    main()