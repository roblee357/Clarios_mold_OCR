import zmqimage, cv2
zmq = zmqimage.zmqImageShowServer(open_port="tcp://*:5555")
print("Starting zmqImageShow Server...")
print("  press Ctrl-C to stop")
i =  0
while True:       # Until Ctrl-C is pressed, will repeatedly
    arrayname, image = zmq.getArray()
    cv2.imshow(arrayname, image)
    cv2.waitKey(1)

    print(i)
    i += 1
