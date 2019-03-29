"""
Robot-Dev Code Version 0.5.1-29032019
This code is design to be used with Raspberry Pi Zero W

*This code is to function as a slave following one master (server)
instructions.
*print function is used for debugging purposes.
*log.write_log are use to keep record of the program

"""
# Direct import
import selectors
import socket
import types

# Partial import
from easylog import EasyLog
from dcmcontrol import DCMControl

# Global variables
name = "Robot 1"
log = EasyLog() # Initialize EasyLog
        
class TCPHandler(): # TCP handler for incoming connection
    """
    Two way communication for multiple connections with multiplexing support.
    Dependencies: selectors, socket and types
    
    *Default port value is 5000 with a buffer size of 4096 bytes
    *To change the value, two arguments need to be pass to the class when
    inheriting or creating an instance.
    *Once initialize both variable are not changeable.
    
    *Data Stream Format: [keyword][data_len][data]
    *Keyword and data_len are pack with struct 
    
    """
    
    conn_cntr = 0
    
    def __init__(self, port=5000, buf_size=4096):
        print("TCPHandler started!")
        # Selectors for multiplexing
        self.sel = selectors.DefaultSelector()
        
        # Set buffer size
        self.buf_size = buf_size
        
        # Variables
        self.IP = self.get_self_IP() # Assign IP
        self.port = port # Assign port
        self.id_cntr = 0
        
        # Using IPv4
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((self.IP, self.port)) # Bind IP and Port for listening
        self.sock.listen(32) # Limit conn to 32 connection
        self.sock.setblocking(False) # No blocking
        self.sel.register(self.sock, selectors.EVENT_READ, data=None)
    
    def get_self_IP(self):
        self.sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.sock2.connect(("8.8.8.8", 80))
            IP = self.sock2.getsockname()[0]
        except:
            IP = "127.0.0.1"
        finally:
            print("Self IP set to", IP)
            self.sock2.close()
        return IP
    
    def check_conn(self):
        # To be called when ready for the next connection and action
        print("Checking connections!")
        try:
            events = self.sel.select(timeout=0) # Check events with no blocking
            for key, mask in events:
                if key.data is None:
                    self._accept_conn(key.fileobj)
                else:
                    self._service_conn(key, mask)
        except:
            print("No connections ready!")
            return
        
    def connect(self, host, port, messages):
        addr = (host, port)
        self.id_cntr+=1
        print('starting connection', connid, 'to', addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(connid=self.id_cntr,
                                     addr=addr,
                                     type="out",
                                     outb=b'')
        sel.register(sock, events, data=data)
    
    def _accept_conn(self, sock):
        conn, addr = self.sock.accept() # Accept connection
        conn.setblocking(False) # No blocking
        self.id_cntr+=1 # Gives conn an id for tracking purposes
        data = types.SimpleNamespace(connid=self.id_cntr,
                                     addr=addr,
                                     key=self.ikey,
                                     outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data)
        TCPHandler.conn_cntr +=1
        print("Accepted connection from", addr, 
              "\nConnection id:", self.id_cntr,
              "\nTotal connections:", TCPHandler.conn_cntr)
        
    def _service_conn(self, key, mask):
        sock = key.fileobj
        data = key.data
        print("Servicing connection:", data.connid, 
              "\nConnection type:", data.type)
        if data.type == "in":
            if mask & selectors.EVENT_READ:
                recv_data = self.sock.recv(self.buf_size)
                if recv_data:
                    data.outb += recv_data
                    self.data_process(recv_data)
                else:
                    print("Closing connection to", data.addr)
                    self.sel.unregister(sock)
                    TCPHandler.conn_cntr -=1
                    sock.close()
            if mask & selectors.EVENT_WRITE:
                if data.outb:
                    print("Echoing", repr(data.outb), "to", data.addr)
                    sent = sock.send(data.outb)
                    data.outb = data.outb[sent:]
        elif data.type == "out":
            if mask & selectors.EVENT_READ:
                recv_data = sock.recv(1024)  # Should be ready to read
                if recv_data:
                    print('received', repr(recv_data), 
                          'from connection', data.connid)
                    data.recv_total += len(recv_data)
                if not recv_data or data.recv_total == data.msg_total:
                    print('closing connection', data.connid)
                    sel.unregister(sock)
                    sock.close()
            if mask & selectors.EVENT_WRITE:
                if not data.outb and data.messages:
                    data.outb = data.messages.pop(0)
                if data.outb:
                    print('sending', repr(data.outb), 
                          'to connection', data.connid)
                    sent = sock.send(data.outb)  # Should be ready to write
                    data.outb = data.outb[sent:]

if __name__ == "__main__":
    pass