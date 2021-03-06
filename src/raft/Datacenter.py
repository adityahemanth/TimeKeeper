'''
Created on 25 May 2016

@author: Johnny
'''
from StateController import StateController
import socket,pickle
import time
from math import ceil
from Log import Log
from LogItem import LogItem
from State import State
import threading
from ClientReqHandler import ClientReqHandler
from Message import Message

class Datacenter(threading.Thread,StateController,ClientReqHandler):
    
    def __init__(self,dc_ID):
        
        super(Datacenter, self).__init__()
#        list=[('0.0.0.0',12346)]
#        list=[("127.0.0.1",8001),("127.0.0.1",8002),("127.0.0.1",8003)]
        list=[("128.111.84.169",8001),("128.111.84.189",8002),("128.111.84.239",8003),\
               ("128.111.84.234",8004),("128.111.84.222",8005)]#         
        dc = [1,2,3]
        State.init(int(dc_ID),len(list),3.0,list,"0.0.0.0",list[int(dc_ID)][1],dc)
    
    def run(self):
        
        while True:
            for dcNum in range(State.numOfDc):
                if(self.periodEnd(time.time(),dcNum) and dcNum!=State.dc_ID):
                    self.onPeriodEnd(dcNum)
            
            if(self.isTimeout(time.time())):
                self.onTimeout()
            
    def listen(self):
        
        tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcpsock.bind((State.host,State.port))
        tcpsock.listen(5)
        print("listening ...")
        
        while True:
            (c, addr) = tcpsock.accept()
            rcv = c.recv(4096)
            message = pickle.loads(rcv)
            mtype = message.getType() 
            
            obj=message.getPayload()
            
            
            if(self.eql(mtype,'AppendEntriesRPC')):
                self.stepDown(obj)
                if(obj.leaderId>=State.numOfDc):
                    pass
                else:
                    self.onRecAppendEntriesRPC(obj)
            elif(self.eql(mtype,'AppendEntriesRPCReply')):
                if(obj.followerId>=State.numOfDc):
                    pass
                else:
                    self.stepDown(obj)
                    self.onRecAppendEntriesRPCReply(obj)
            elif(self.eql(mtype,'RequestVoteRPC')):
                if(obj.candidateId>=State.numOfDc):
                    pass
                else:
                    self.stepDown(obj)
                    self.onRecReqVoteRPC(obj)
            elif(self.eql(mtype,'RequestVoteRPCReply')):
                if(obj.voterId>=State.numOfDc):
                    pass
                else:
                    self.stepDown(obj)
                    self.onRecReqVoteRPCReply(obj)
            elif(self.eql(mtype, 'CreatePost')):
                self.onRecCreatePostReq(obj,c)
            elif(self.eql(mtype,'Lookup')):
                msg=Message('LookupReply',State.log)
                c.send(pickle.dumps(msg,0))
            elif(self.eql(mtype,'LookupLog')):
                msg=Message('LookupReply',State.log)
                c.send(pickle.dumps(msg,0))
            elif(self.eql(mtype, 'GetDcId')):
                c.send(State.dc_Id)
            elif(self.eql(mtype,'ConfigChange')):
                self.onRecConfigChangeReq(obj, c)
            else:
                print('Invalid message type!!!')  
            
            
            #print(mtype)
            c.close()
            
    def config(self):
        elements=self.inputList("Input config:")
        self.dc_list = list(elements)
        print(self.dc_list)
        print(self.dc_ID)
        (self.host,self.port) = self.dc_list[self.dc_ID]      
    def inputList(self,yourComment):
        listSTR=input(yourComment)     
        listSTR =listSTR[1:len(listSTR)-1]
        listT = listSTR.split(",")
        listEnd=[]
        for caseListT in listT:
            listEnd.append(int(caseListT))
        return listEnd
        
def main():
        
    ID = input ("$ datacenter ID:")
    
    dc = Datacenter(ID)
    dc.start()
    dc.listen()       

if __name__ == "__main__":
    main()
    
        

        
