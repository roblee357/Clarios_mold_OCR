from ctypes import create_string_buffer
import sys, json, pickle
import zmq
import numpy as np
import time, cv2


#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Collecting updates from weather server...")
socket.connect("tcp://localhost:5555")
zip_filter = 'raw'
socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)

t = time.time()
while True:
    string = socket.recv_string()
    # data = socket.recv()
    topiclen = len(string.split(' ')[0]) + 1
    topic = string[0:topiclen]
    msg = string[topiclen:]
    data = json.loads(msg)
    # pickle.load(
    img = np.array(data['data'], dtype=np.uint8)
    print(topic, data['dtype'], img.shape, time.time()-t)
    t = time.time()
    cv2.imshow('raw',img)
    key = cv2.waitKey(1) & 0xFF



