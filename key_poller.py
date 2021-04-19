from pynput.keyboard import Key, Listener
import time
from threading import Thread

class Key_listener():

    def __init__(self):
        self.queue = [2,1,1,1,1,1,1,1]
        self.itime = time.time()
        self.scanned = False

        start_thread = Thread(target=self.start)
        start_thread.start()

    def on_press(self,key):
        try:
            if key.char in '0123456789':
                # print('key char',key.char)
                self.queue.append(time.time() - self.itime)
                self.queue.pop(0)
                # print(self.queue)
                self.itime = time.time()
            if self.queue[1] < .005:
                print("scan detected")
                self.queue = [2,1,1,1,1,1,1,1]
                self.scanned = True
        except:
            pass        
    def start(self):        
        with Listener(on_press=self.on_press) as listener:
            listener.join()
    
    def reset(self):
        self.scanned = False

def main():
    kl = Key_listener()
    # kl.start()
    while True:

        print(kl.scanned)

        if kl.scanned:
            kl.reset()
        time.sleep(1)

if __name__ == '__main__':
    main()




