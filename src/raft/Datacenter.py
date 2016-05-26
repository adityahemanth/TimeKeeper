'''
Created on 25 May 2016

@author: Johnny
'''
from StateController import StateController
import socket,pickle

class Datacenter(StateController):
    
    def __init__(self,id,numOfDC,majorityNum,timeUnit):
        self.currentTerm=1
        self.log=[]
        self.commitIndex=-1
        self.lastApplied=-1
        self.state='follower'
        self.id=id
        self.numOfDC=numOfDC
        self.majorityNum=majorityNum
        self.timeUnit=timeUnit
    
    def listen(self):
        
        tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        tcpsock.bind((self.host,self.port))
        tcpsock.listen(5)
        print("listening ...")
        
        while True:
            (c, addr) = tcpsock.accept()
            rcv = c.recv(4096)
            message = pickle.loads(rcv)
            mtype = message.getType() 
            
            self.stepDown(message)
            
            if(self.eql(mtype,'AppendEntriesRPC')):
                self.onRecAppendEntriesRPC(self.state, message)
            elif(self.eql(mtype,'AppendEntriesRPCReply')):
                self.onRecAppendEntriesRPCReply(message)
            elif(self.eql(mtype,'RequestVoteRPC')):
                self.onRecReqVoteRPC(self.state, message)
            elif(self.eql(mtype,'RequestVoteRPCReply')):
                self.onRecReqVoteRPCReply(message)
            else:
                print('Invalid message type!!!')  
        
    def config(self):
        self.dc_list = input("Input config:")
        print(self.dc_list)
        print(self.dc_ID)
        (self.host,self.port) = self.dc_list[self.dc_ID]      
          
    def setDcList(self,dc_list):
        self.dc_list = dc_list
        (self.host,self.port) = self.dc_list[self.dc_ID]
        
    def setHost(self,host):
        self.host=host
    def setPort(self,port):
        self.port=port
        
        

        