'''
Created on 25 May 2016

@author: Johnny
'''
from StateController import StateController
import socket,pickle
from Follower import Follower
from time import time
from math import ceil
from Log import Log
import LogItem

class Datacenter(StateController):
    
    def __init__(self,dc_ID,numOfDC,timeUnit):
        
        self.commitIndex=-1
        self.lastApplied=-1
        
        self.dc_ID=dc_ID
        self.numOfDC=numOfDC
        self.majorityNum=ceil(1.0*self.numOfDC/2.0)
        self.timeUnit=timeUnit
        
        self.state='follower'
        self.log=Log()
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
            if(self.periodEnd(time.time())):
                self.onPeriodEnd()
            
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
    
def main():
        
    ID = input ("$ datacenter ID:")
    numOfDC = input ("$ datacenter number:")
    timeUnit = input ("$ timeUnit:")
    
    dc = Datacenter(ID,numOfDC,timeUnit)
    dc.config()
    dc.listen()
        
    if __name__ == "__main__":
        main()
    
        

        