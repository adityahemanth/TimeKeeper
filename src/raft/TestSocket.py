'''
Created on 30 May 2016

@author: Johnny
'''
import socket
from Sender import Sender
from Message import Message
import threading

class TestSocket(threading.Thread):
    
    def __init__(self):
        super(TestSocket, self).__init__()
    
    def send(self):
        sender=Sender('TestMessage','Hello')
        sender.send(('0.0.0.0',12345))            
    
    
    def listen(self):
        tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcpsock.bind(('0.0.0.0',12345))
        tcpsock.listen(5)
        print("listening ...")
        
        self.start()
        
    def run(self):
        
        while True:
            self.send()
            
def main():
    
    ts=TestSocket()
    ts.listen()
if __name__ == "__main__":
    main()    