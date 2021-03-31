#! python3
import pyautogui, sys, keyboard, time, json, os, win32clipboard
from tkinter import *
import win_loc

global wormhole_active, CBdata, prev_x, prev_y, config

keyboard.is_pressed('F8')
configPath = 'config.json'
configExists = os.path.exists(configPath)

if keyboard.is_pressed('F8') or not configExists:
    input("Move cursor to top left corner of region to be blocked and press enter.")
    topLeft = pyautogui.position()
    print(topLeft)
    input("Move cursor to lower right corner of region to be blocked and press enter.")
    bottomRight = pyautogui.position()
    print(bottomRight)
    right_pos = topLeft[0]
    down_pos = topLeft[1]
    win_width = bottomRight[0] - topLeft[0]
    win_height = bottomRight[1] - topLeft[1]
    config = {    "right_pos" : right_pos,"down_pos" : down_pos, "win_width" : win_width, "win_height" : win_height}
    with open(configPath,'w') as fout:
        json.dump(config,fout)
else:
    with open(configPath,'r') as fin:
        config = json.load(fin)
        bs_pos = win_loc.main()
        right_pos = bs_pos[0] + bs_pos[2] - config["win_width"] -20
        down_pos = bs_pos[1] + 265
        win_width = config["win_width"]
        win_height = config["win_height"]
        
prev_x, prev_y = 0,0
win_width_s = str(win_width) + 'x'
win_height_s = str(win_height) + '+'
right_pos_s = str(right_pos) + '+'
down_pos_s = str(down_pos)
wormhole_active = True

def openNewWindow():
    global wormhole_active
    wormhole_active = not wormhole_active
    print('clicked')

def getCBdata():
    try:
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)
        win32clipboard.CloseClipboard()
    except:
        data = ""
    return data
CBdata = getCBdata()

def enter_field(moldNo):
    curPos = pyautogui.position()
    right_pos = config["right_pos"]
    down_pos = config["down_pos"]
    win_width = config["win_width"]
    win_height = config["win_height"]
    root.withdraw()
    windowCenterX = right_pos + win_width / 2
    windowCenterY = down_pos + win_height / 2
    pyautogui.moveTo(windowCenterX, windowCenterY)
    pyautogui.click()
    try:
        moldNo = moldNo.decode("utf-8")
    except:
        moldNo = moldNo
    print(moldNo, right_pos)
    pyautogui.write(moldNo,.02)
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.moveTo(curPos[0], curPos[1])
    root.update()
    root.deiconify()
root = Tk()
root.configure(bg='blue')
root.overrideredirect(1)
root.geometry(win_width_s + win_height_s + right_pos_s + down_pos_s)
root.attributes('-alpha', 0.3)
root.lift()
root.attributes('-topmost', True)
btn = Button(root,  
             text ="",  # Hardest button to button
             command = openNewWindow,
             background='blue') 
btn.pack(fill=BOTH, expand=1) 

def task():
    global wormhole_active, prev_x, prev_y, CBdata
    x, y = pyautogui.position()
    positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4) + '\n'
#### Uncomment to view position
##    print(positionStr, end='')
    xcheck = x >= right_pos and x <= right_pos + win_width
    ycheck = y >= down_pos and y <= down_pos + win_height
    prev_x, prev_y = x, y 
    root.after(1, task)
root.after(1, task)
root.mainloop()
