#!/usr/bin/python           # This is client.py file

from __future__ import print_function
import pickle
from Message import *
from Post import *
import socket               # Import socket module
from Log import Log
from LogItem import LogItem 

class Client(object):
    
    def __init__(self,dc_Id):
        
        list=[("128.111.84.169",8001),("128.111.84.189",8002),("128.111.84.239",8003),\
               ("128.111.84.234",8004),("128.111.84.222",8005)]
        
        self.dc_list=list 
        self.numOfDc=len(self.dc_list)
        self.versionNumber=0
        self.dc_Id=dc_Id
        self.leaderId=self.dc_Id
        
        
    def lookup(self):
        s = socket.socket()
        
        conn = self.dc_list[self.dc_Id]
        msg = Message('Lookup', None)
            
        send = pickle.dumps(msg,0)
            
        s.connect(conn)
        s.send(send)
        rcv = s.recv(4096)
        
        msg= pickle.loads(rcv)
        log=msg.getPayload()
        print("Local datacenter: ")
        log.displayPosts()
        
        s.close()
    def configChange(self):
        s = socket.socket()
        
        dc_no = int(input('$ DC ID: '))
        
        msg = Message('ConfigChange', dc_no)
            
        send = pickle.dumps(msg,0)
        
        for dcNum in range(self.numOfDc):
            s = socket.socket()
        
            conn = self.dc_list[dcNum]
            try:    
                s.connect(conn)
                success=True
            
            except Exception as e:
                print("No connection! From DC "+str(dcNum))
                success=False
                continue
            finally:
                if(success):
                    s.send(send)
                    rcv = s.recv(4096)
                    print(pickle.loads(rcv))
                    
                s.close()
                
    def lookupLog(self):
        s = socket.socket()
        
        dcNum = input("Enter datacenter number: ")
        dcNum=int(dcNum)
        
        conn = self.dc_list[dcNum]
        msg = Message('LookupLog', None)
        send = pickle.dumps(msg,0)
            
        s.connect(conn)
        s.send(send)
        rcv = s.recv(4096)
            
        msg= pickle.loads(rcv)
        log=msg.getPayload()
        print("Datacenter: "+str(dcNum))
        log.display()
        
        s.close()
        
    def createPost(self):
        
        pst = input("Enter post: ")
        self.incrementVersionNumber()
        p = Post(self.dc_Id, pst, self.versionNumber)
        msg = Message('CreatePost', p)
        
        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            
            conn = self.dc_list[self.leaderId]
            sendMsg = pickle.dumps(msg,0)
            
            try:
                s.connect(conn)
                success=True
            
            except Exception as e:
                print("No connection! From DC "+str(self.leaderId))
                print(e)
                success=False
                self.nextLeaderId()
                s.close()
                continue
            
            finally:
                if(success):
                    s.send(sendMsg)
                    rcv = s.recv(4096)
                    rcvMsg = pickle.loads(rcv)
                    if(rcvMsg):
                        print("Accepted! By DC "+str(self.leaderId))
                        break
                    else:
                        print("Denied! By DC "+str(self.leaderId))
                        self.nextLeaderId()
                s.close();
                    
    def nextLeaderId(self):
        self.setLeaderId((self.leaderId+1) % (self.numOfDc))
    
    def setLeaderId(self,leaderId):
        self.leaderId=leaderId
    
    def incrementVersionNumber(self):
        self.versionNumber=self.versionNumber+1 
    
    def getDcId(self, host, port):
        
        s = socket.socket() 
        conn = (host,port)
        
        msg = Message("GetDcId", None)
        send = pickle.dumps(msg,0)
        
        s.connect(conn)
        s.send(send)
        
        rcv = s.recv(4096)
        return int(rcv)
    

def main():
    
    ID = input ("$ hostIP: ")
    #port = input("$ port: ")
    #port = int(port)
    #current_Dc_no = getInfo(str(ID), port)
    client=Client(int(ID));
    
    print("Connected to DataCenter: ", end = "")
    print(ID)

    while True:

        ipt = input("$ ")
        if(ipt == "lookup"):
            client.lookup()

        elif(ipt == "post"):
            client.createPost()

        elif(ipt == "lookuplog"):
            client.lookupLog()
        elif(ipt == "configChange"):
            client.configChange()
        else:
            print("invalid input")



if __name__ == "__main__":
    main()




