import socket
import pickle
import threading
from Message import Message

class Sender(threading.Thread):
    
    def __init__(self,type,obj):
        
        threading.Thread.__init__(self)
        self.type=type
        self.obj=obj
    
    def setConn(self,conn):
        self.conn=conn
    
    def run(self):
        self.send(self.conn);
    
    def send(self, conn):
        s = socket.socket()
        m = Message(self.type, self.obj)
        try:
            s.connect(conn) 
            success=True
            # originally, it was 
            # except Exception, e: 
            # but this syntax is not supported anymore. 
        except Exception as e: 
            success=False
        finally:
            if(success):
                s.send(pickle.dumps(m,0))
            s.close()
    
    