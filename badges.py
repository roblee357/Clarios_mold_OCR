import pandas as pd
import tkinter, datetime, pyautogui, time

class Badge:
    def __init__(self, master):
        self.master = master
        self.path = 'badges.csv'
        self.df = pd.read_csv(self.path,index_col='index')  # ,header=None , comment = '#',names=["code", "firstname", "lastname", "date_added"]

    def prt(self):
        print(self.df)

    def lookupName(self,scan_input):
        self.scan_input = scan_input
        fisrtnames = self.df.loc[self.df['code'] == scan_input]['firstname']
        lasttnames = self.df.loc[self.df['code'] == scan_input]['lastname']
        if len(fisrtnames) > 0:
            return fisrtnames.iloc[0], lasttnames.iloc[0] 
        else:
            print('badge not found')
            return self.addName()

    def addName(self):
        # master = tkinter.Tk()
        self.nameRequestWindow = tkinter.Toplevel(self.master)
        self.nameRequestWindow.title("New Badge. Please type name.")
        self.nameRequestWindow.lift()
        self.nameRequestWindow.focus()
        self.nameRequestWindow.grab_set()  #for disable main window
        self.nameRequestWindow.attributes('-topmost',True)  #for focus on toplevel
        self.nameRequestWindow.focus_force()
        e = tkinter.Entry(self.nameRequestWindow)
        e.pack(padx=120, pady=40)
        e.focus_set()
        def callback(event = None):
            self.nameInput = e.get() # This is the text you may want to use later
            self.nameRequestWindow.destroy()
        b = tkinter.Button(self.nameRequestWindow, text = "OK", width = 10, command = callback)
        b.pack()
        self.nameRequestWindow.bind('<Return>', callback) 
        self.master.wait_window(self.nameRequestWindow)
        self.now = datetime.datetime.now()
        self.ts = self.now.strftime("%Y_%m_%d___%H_%M_%S")
        self.firstnameInput = self.nameInput.split(' ')[0]
        self.lastnameInput = self.nameInput.split(' ')[1]
        self.df.loc[len(self.df.index)+1] = [ self.scan_input,self.firstnameInput,self.lastnameInput ,self.ts]
        print(self.df)
        self.df.to_csv(self.path,index=True)
        return  self.firstnameInput, self.lastnameInput

    def scan(self):
        self.badgeScanWindow = tkinter.Toplevel(self.master)
        self.badgeScanWindow.lift()
        self.badgeScanWindow.focus()
        self.badgeScanWindow.grab_set()  #for disable main window
        self.badgeScanWindow.attributes('-topmost',True)  #for focus on toplevel
        self.badgeScanWindow.focus_force()
        self.badgeScanWindow.title("Scan your badge.")
        self.badgeScanText = tkinter.StringVar(self.badgeScanWindow, value="Scan badge")
        self.badgeScan = tkinter.Entry(self.badgeScanWindow, textvariable = self.badgeScanText)
        self.badgeScan.pack(padx=100, pady=50)
        self.badgeScanWindow.after(1000, self.sendTab)
        self.badgeScanWindow.bind('<Return>', self.badgeAccepted) 
        self.master.wait_window(self.badgeScanWindow)

    def badgeAccepted(self, e):
        print('badgeScanWindow destroyed')
        self.badgeNo = self.badgeScan.get() 
        self.lookedUpName = self.lookupName(self.badgeNo)
        print('self.lookedUpName',self.lookedUpName)
        self.badgeScanWindow.destroy()        

    def sendTab(self):
        pyautogui.press('tab')
        print('sent tab')

def main():
    master = tkinter.Tk()
    badges = Badge(master)
    badgeName = badges.scan()
    # badges.prt()
    print('badgeName',badgeName)

if __name__ == '__main__':
    main()
