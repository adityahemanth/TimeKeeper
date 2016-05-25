import socket
import pickle
import Message
class Sender:
    
    def __init__(self,type,obj):
        self.type=type
        self.obj=obj
    
    def send(self, conn):
        s = socket.socket()
        m = Message(self.type, self.obj)
        s.connect(conn)
        s.send(pickle.dumps(m,0))
        s.close()
    
    