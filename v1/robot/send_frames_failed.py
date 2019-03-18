#send_frames

import cv2
import numpy as np
import time
import socket

# Set up video feed
cap = cv2.VideoCapture(0)
key = cv2.waitKey(1) & 0xFF

# Set up TCP
TCP_IP = '192.168.1.225'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))

while True:
    s.listen(1)
    conn, addr = s.accept()
    print("Connection from: ", addr)
    ret, frame = cap.read()
    
    if ret:
        s.send(frame)
        if key == ord('q'):
            break

conn.close()

