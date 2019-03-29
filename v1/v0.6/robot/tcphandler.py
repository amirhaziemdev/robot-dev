import selectors
import struct
import socket
import types
import time

class TCPHandler(): # TCP handler for incoming connection
    """
    Two way communication for multiple connections with multiplexing support.
    Dependencies: selectors, struct, socket, types and time
    
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
        self.IP = self.get_self_local_IP() # Assign IP
        self.port = port # Assign port
        self.id_cntr = 0
        self.conn_list = []
        self.conn_ctrl = []
        self.buffer = []
        
        # Using IPv4 for listening to connection
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.IP, self.port)) # Bind IP and Port for listening
        self.sock.listen(32) # Limit conn to 32 connection
        self.sock.setblocking(False) # No blocking
        self.sel.register(self.sock, selectors.EVENT_READ, data=None)
    
    def get_self_local_IP(self):
        # Get self local IP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        try:
            # Doesn't matter if cannot connect
            sock.connect(("192.168.1.1", 1))
            IP = sock.getsockname()[0]
        except:
            IP = "127.0.0.1"
        finally:
            print("Self IP set to", IP)
            sock.close()
            
        return str(IP)
    
    def check_conn(self):
        # To be called when ready for the next connection and action
        print("Checking connections!")
        
        events = self.sel.select(timeout=0) # Check events with no blocking
        if events:
            for key, mask in events:
                if key.data is None:
                    self._accept_conn(key.fileobj)
                else:
                    self._service_conn(key, mask)
            return 0
        else:
            print("No connections ready!")
            return 1
        
    def create_conn_data(self, addr, type, key=0, data_out=""):
        # To create data describing the connection
        self.id_cntr+=1 # Gives conn an id for tracking purposes
        
        data_outb = bytes(data_out, "utf-8")
        data_len = len(data_outb) # Calc data length
        
        data = types.SimpleNamespace(connid=self.id_cntr,
                                     addr=addr,
                                     type=type,
                                     status="ready",
                                     key=key,
                                     key_pack=struct.pack(">L", key),
                                     data=data_out,
                                     datal=data_len,
                                     datal_pack=struct.pack(">L", data_len),
                                     outb=b"",
                                     last_mod=time.time())
        
        return data

    def connect(self, host, port, key, data_out):
        addr = (host, port)
        type = "out"
        
        # Create new socket object for every connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        
        # Create conn data
        data = self.create_conn_data(addr, type, key, data_out)
        
        # Register event
        self.sel.register(sock, events, data=data)
        
        # Increment conn_cntr + debugging print
        TCPHandler.conn_cntr +=1
        print('Starting connection', data.connid, 'to', addr)
                               
        # Return conn id
        return self.id_cntr
    
    def _accept_conn(self, sock):
        type = "in"
        
        # Accepting connection
        conn, addr = self.sock.accept()
        conn.setblocking(False)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        
        # Create conn data
        data = self.create_conn_data(addr, type)
        
        # Register event
        self.sel.register(conn, events, data=data)
        
        # Increment conn_cntr + debugging print
        TCPHandler.conn_cntr +=1
        print("Accepted connection from", addr, 
              "\nConnection id:", self.id_cntr,
              "\nTotal connections:", TCPHandler.conn_cntr)
        
    def _service_conn(self, key, mask):
        sock = key.fileobj # Get socket object
        data = key.data # Get conn description
        
        # Calc struct packing size for unsigned long
        # For unpacking keyword and data_len
        pack_size=struct.calcsize(">L")
        
        # Debugging print
        print("Servicing connection:", data.connid, 
              "\nConnection type:", data.type)
        
        # Servicing connection
        # If time elapsed without changing is equal to 10s close socket
        time_elapsed = time.time() - data.last_mod
        print(time_elapsed)
        if time_elapsed > 10:
            # Decrement conn_cntr + debugging print
            TCPHandler.conn_cntr -=1
            print("Closing connection to", data.addr,
                  "\nTotal connections:", TCPHandler.conn_cntr)
            
            # Unregister event
            self.sel.unregister(sock)
            
            # Close connection
            sock.close()
        # If ready for reading data
        if data.type == "in":
            # Save data from buffer
            try:
                recv_data = sock.recv(self.buf_size)
            except:
                return
            
            # If there is data in buffer
            if recv_data:
                # Put everything in data.outb
                data.outb += recv_data
                
                # Get pack key value
                data.key_pack = data.outb[:pack_size]
                # Filter data.outb
                data.outb = data.outb[pack_size:]
                
                # Get pack data length value
                data.datal_pack = data.outb[:pack_size]
                # Filter data.outb
                data.outb = data.outb[pack_size:]
                
                # Unpacking
                data.key = struct.unpack(">L", data.key_pack)[0]
                data.datal = struct.unpack(">L", data.datal_pack)[0]
                
                # Get the rest of data
                print(len(data.outb))
                print(data.datal)
                while len(data.outb) < data.datal:
                    data.outb += sock.recv(self.buf_size)
                
                # Save data to data.data
                data.data = data.outb[:data.datal]
                # Empty data.outb
                data.outb = b""
                
                print(data)
                print(sock)
                
                # Pass data to be process and sock to easily manipulate
                # selectors later
                self.buffer.append([data, sock])
                
                # Expecting to send back data
                data.type = "out"
                data.status = "pending"
                
                data.last_mod = time.time()
                
                # Replace event data with latest update
                events = selectors.EVENT_READ | selectors.EVENT_WRITE
                self.sel.modify(sock, events, data=data)
            
            # Else close the connection
            else:
                # Decrement conn_cntr + debugging print
                TCPHandler.conn_cntr -=1
                print("Closing connection to", data.addr,
                      "\nTotal connections:", TCPHandler.conn_cntr)
                
                # Unregister event
                self.sel.unregister(sock)
                
                # Close connection
                sock.close()
        
        # If ready for sending data
        elif data.type == "out" and data.status == "ready":
            # If data exist to be sent
            if data.data:
                data.outb += data.key_pack
                data.outb += data.datal_pack
                data.outb += bytes(data.data, "utf-8")
                data.data = ""
                print("Sending", repr(data.outb), "to", data.addr)
                try:
                    sent = sock.sendall(data.outb)
                except:
                    print("Failed to send data to", data.addr)
                data.type = "in"
                data.outb = data.outb[sent:]
                data.last_mod = time.time()
                
                # Replace event data with latest update
                events = selectors.EVENT_READ | selectors.EVENT_WRITE
                self.sel.modify(sock, events, data=data)
            
            # Else close the connection
            else:
                # Decrement conn_cntr + debugging print
                TCPHandler.conn_cntr -=1
                print("Closing connection to", data.addr,
                      "\nTotal connections:", TCPHandler.conn_cntr)
                
                # Unregister event
                self.sel.unregister(sock)
                
                # Close connection
                sock.close()
        else:
            # Decrement conn_cntr + debugging print
            TCPHandler.conn_cntr -=1
            print("Closing connection to", data.addr,
                  "\nTotal connections:", TCPHandler.conn_cntr)
            
            # Unregister event
            self.sel.unregister(sock)
            
            # Close connection
            sock.close()
    
    def get_buffer_data(self):
        return self.buffer
    
    def ready_data(self, buffer_index, key, data_out):
        # buffer format [[data,sock],[data,sock]]
        # Remove ready data from buffer
        get_buffer = self.buffer.pop(buffer_index)
        
        # Variables
        sock = get_buffer[1]
        data = get_buffer[0]
        
        # Get new data length
        data_outb = bytes(data_out, "utf-8")
        data_len = len(data_out)
        
        # Edit data vars
        data.key = key
        data.data = data_out
        data.datal = data_len
        data.type = "out"
        data.status = "ready"
        data.last_mod = time.time()
        # Pack
        data.key_pack = struct.pack(">L", key)
        data.datal_pack = struct.pack(">L", data_len)
        
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        
        self.sel.modify(sock, events, data=data)
    
    def close_conn(self, buffer_index, key, data_out):
        # buffer format [[data,sock],[data,sock]]
        # Remove ready data from buffer
        get_buffer = self.buffer.pop(buffer_index)
        
        # Variables
        sock = get_buffer[1]
        data = get_buffer[0]
        
        # Get new data length
        data_outb = bytes(data_out, "utf-8")
        data_len = len(data_out)
        
        # Edit data vars
        data.key = key
        data.data = data_out
        data.datal = data_len
        data.type = "close"
        data.status = "ready"
        data.last_mod = time.time()
        # Pack
        data.key_pack = struct.pack(">L", key)
        data.datal_pack = struct.pack(">L", data_len)
        
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        
        self.sel.modify(sock, events, data=data)
    
    def __del__(self):
        self.sel.close()