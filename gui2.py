from io import RawIOBase
import capture, preprocess, OCR
import time, cv2


cap = capture.Capture(1)
print('before run')
cap.start()
t = time.time()
while cap.img is None:
    print('waiting for camera to connect',time.time()-t)
    time.sleep(.25)

proc = preprocess.Processor()
proc.start(cap)
while proc.img is None:
    print('waiting for processed image',time.time()-t)
    time.sleep(.25)


ocr = OCR.OCR()
ocr.start(proc)

while ocr.txt is None:
    print('waiting for OCR',time.time()-t)
    time.sleep(.25)

t = time.time()

while True:
    raw = cap.img
    processed = proc.img
    # cv2.imshow('this',raw)
    cv2.imshow('this',processed)

    cv2.waitKey(1)
    print(ocr.txt,'Running',time.time()-t)
    t = time.time()