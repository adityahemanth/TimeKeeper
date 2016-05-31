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
            s.send(pickle.dumps(m,0))
            # originally, it was 
            # except Exception, e: 
            # but this syntax is not supported anymore. 
        except Exception as e: 
            print("something's wrong with %s:%d. Exception is %s" % (conn[0], conn[1], e))
        finally:
            s.close()
    
    