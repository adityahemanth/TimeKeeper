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

class Datacenter(threading.Thread,StateController):
    
    def __init__(self,dc_ID,numOfDc,timeUnit):
        
        super(Datacenter, self).__init__()
        list=[('0.0.0.0',12346)]
#         list=[('0.0.0.0',12346),('0.0.0.0',12347),('0.0.0.0',12348),\
#               ('0.0.0.0',12349),('0.0.0.0',12350)]
        State.init(dc_ID,numOfDc,timeUnit,list)
    
    def run(self):
        
        while True:
            
            if(self.isTimeout(time.time())):
                print("Time out!")
                self.onTimeout()
            if(self.periodEnd(time.time())):
                print("Period end!")
                self.onPeriodEnd()
            
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
            
            self.stepDown(message)
            
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
    numOfDc = input ("$ datacenter number:")
    timeUnit = input ("$ timeUnit:")
    
    dc = Datacenter(ID,numOfDc,timeUnit)
    dc.start()
    dc.listen()
        
if __name__ == "__main__":
    main()
    
        

        