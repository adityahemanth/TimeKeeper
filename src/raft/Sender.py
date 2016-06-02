import socket
import pickle
from Message import Message
class Sender(object):
    
    def __init__(self,type,obj):
        self.type=type
        self.obj=obj
    
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
    
    