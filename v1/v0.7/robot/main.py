"""
main_robot.py
Robot-Dev Code Version 0.7.0-01042019
This code is design to be used with Raspberry Pi Zero W

*This code is to function as a slave following one master (server)
instructions.
*print function is used for debugging purposes.
*log.write_log are use to keep record of the program

"""
# Direct import
import cv2
import pickle

# Partial import
from easylog import EasyLog
#from dcmcontrol import DCMControl
from tcphandler import TCPHandler

# Global variables
name = "Robot 1"
log = EasyLog() # Initialize EasyLog

# Camera
cap = cv2.VideoCapture(0)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

def cmd_exec(cmd):
    if cmd == "frame":
        ret, frame = cap.read()
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pass
        result, frame = cv2.imencode('.jpg', frame, encode_param)
        data = pickle.dumps(frame, 0)
        return data
    return ""

def process_data(data):
    print(data.key)
    if data.key == 1:
        data.key = 2
        data.data = "Connection established!"
        return data
    elif data.key == 1000:
        data.data = data.data.decode("utf-8")
        print(data.data)
        data.data = cmd_exec(data.data)
        data.key = 1001
        return data
    return data

if __name__ == "__main__":
    conn = TCPHandler()
    while True:
        ret = conn.check_conn()
        if not ret:
            buffer = conn.get_buffer_data()
            if buffer:
                for each in buffer:
                    data = each[0]
                    data = process_data(each[0])
                    conn.ready_data(buffer.index(each), data.key, data.data)