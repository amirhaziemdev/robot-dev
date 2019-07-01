"""
main_server.py
Robot-Dev Code Version 0.7.0-01042019
This code is design to be used with a windows computer

*This code is to function as a master giving instruction to many slaves.
*print function is used for debugging purposes.

"""
import cv2
import pickle

from easylog import EasyLog
from tcphandler import TCPHandler


key = cv2.waitKey(0) & 0xFF

class RobotMaster():
    pass

def proc_reply(data):
    cv2.namedWindow('ImageWindow')
    # print(data)
    try:
        frame=pickle.loads(data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        cv2.imshow('ImageWindow',frame)
        if key == ord('q'):
            pass
    except:
        print("Error: frame not shown")
        pass

def process_data(data):
    # print(data.key)
    if data.key == 1:
        data.key = 2
        data.data = "Connection established!"
        return data
    elif data.key == 2:
        data.key = 1000
        data.data = "frame"
        return data
    elif data.key == 1000:
        data.data = data.data.decode("utf-8")
        #data.data = cmd_exec(data.data)
        data.key = 1001
        return data
    elif data.key == 1001:
#         if data.data.decode("utf-8") == "frame":
#             return data
        proc_reply(data.data)
        data.key = 1000
        data.data = "frame"
        return data
    return data

if __name__ == "__main__":
    conn = TCPHandler(port=5001)
    conn.connect("192.168.1.227", 5000, 1, "Handshake")
    while True:
        ret = conn.check_conn()
        if not ret:
            buffer = conn.get_buffer_data()
            print(buffer)
            if buffer:
                for each in buffer:
                    data = each[0]
                    data = process_data(each[0])
                    conn.ready_data(buffer.index(each), data.key, data.data)