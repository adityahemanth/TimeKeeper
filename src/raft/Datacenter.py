'''
Created on 25 May 2016

@author: Johnny
'''
from StateController import StateController
import socket,pickle
from Follower import Follower
from time import time

class Datacenter(StateController):
    
    def __init__(self,id,numOfDC,majorityNum,timeUnit):
        self.log=[]
        self.commitIndex=-1
        self.lastApplied=-1
        
        self.id=id
        self.numOfDC=numOfDC
        self.majorityNum=majorityNum
        self.timeUnit=timeUnit
        
        self.state='follower'
        Follower.reset(1)
        
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
            if(self.isTimeout(time.time())):
                self.onTimeout()
            
            if(self.eql(mtype,'AppendEntriesRPC')):
                self.onRecAppendEntriesRPC(message)
            elif(self.eql(mtype,'AppendEntriesRPCReply')):
                self.onRecAppendEntriesRPCReply(message)
            elif(self.eql(mtype,'RequestVoteRPC')):
                self.onRecReqVoteRPC(message)
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
        
        

        