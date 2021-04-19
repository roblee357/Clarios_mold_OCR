import win32gui

def callback(hwnd, pos):
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    if 'PSMII Bluesheet' in win32gui.GetWindowText(hwnd):
        # print("Window %s:" % win32gui.GetWindowText(hwnd))
        # print("\tLocation: (%d, %d)" % (x, y))
        # print("\t    Size: (%d, %d)" % (w, h))
        pos.append(x)
        pos.append(y)
        pos.append(w)
        pos.append(h)


def main():
    pos = []
    win32gui.EnumWindows(callback, pos)
    # print(pos)
    return pos

if __name__ == '__main__':
    main()