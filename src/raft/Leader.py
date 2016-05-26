from StateController import StateController
from RequestVoteRPCReply import RequestVoteRPCReply 
from RequestVoteRPC import RequestVoteRPC 
from AppendEntriesRPCReply import AppendEntriesRPCReply
from AppendEntriesRPC import AppendEntriesRPC
from Sender import Sender
from Receiver import Receiver
class Leader(StateController,Receiver):
    def reset(self):
        self.onPeriodEnd()
        self.setTimer()
        self.resetNextIndex()
        
    def resetNextIndex(self):
        for dcNum in range(self.numOfDC):
            self.nextIndex[dcNum]=self.log.getLastIndex()+1
            self.matchIndex[dcNum]=0
    
    def decrementNextIndex(self,dcNum):
        self.nextIndex[dcNum]=self.nextIndex[dcNum]-1
    
    def incrementNextIndex(self,dcNum):
        self.nextIndex[dcNum]=self.nextIndex[dcNum]+1
    
    def setMatchIndex(self,dcNum,matchIndex):
        self.matchIndex[dcNum]=matchIndex
    
    def heartbeat(self,dcNum):
        
        return AppendEntriesRPC(self.currentTerm,\
                                self.dc_ID,self.nextIndex[dcNum]-1,\
                                self.log.getTerm(self.nextIndex[dcNum]-1),\
                                None,self.commitIndex)
    
    def entry(self,dcNum):
        
        return AppendEntriesRPC(self.currentTerm,\
                                self.dc_ID,self.nextIndex[dcNum]-1,\
                                self.log.getTerm(self.nextIndex[dcNum]-1),\
                                self.log.getLogItem(self.nextIndex[dcNum]),\
                                self.commitIndex)
    
    def sendAppendEntriesRPC(self):
        
        for dcNum in range(self.numOfDC):
            if(self.isSelf(dcNum)):
                continue
            if(self.matchIndex[dcNum]!=0):
                sender=Sender('AppendEntriesRPC',self.entry(dcNum))
                sender.send(self.dc_list[dcNum])
            else:
                sender=Sender('AppendEntriesRPC',self.heartbeat(dcNum))
                sender.send(self.dc_list[dcNum])            
            
    def isSelf(self,dcNum):
        return (self.dc_ID==dcNum)
    
    def onRecAppendEntriesRPCReply(self,message):
        
        if(not message.success):
            self.decrementNextIndex(message.followerId)
            print("("+str(self.dc_ID)+","+self.state+","+str(self.currentTerm)+'): Retry AppendEntriesRPC to datacenter '+\
                  str(message.followerId))
            sender=Sender('AppendEntriesRPC',self.heartbeat(message.followerId))
            sender.send(self.dc_list[message.followerId])            
            self.setPeriod()
        else:
            self.setMatchIndex(message.followerId, message.matchIndex)
            self.incrementNextIndex(message.followerId)
            if(message.matchIndex>self.commitIndex):
                self.checkCommit(message.matchIndex)
    
    def checkCommit(self,N):
        count=0
        for dcNum in range(self.numOfDC):
            if(self.matchIndex[dcNum]>=N or self.isSelf(dcNum)): 
                count=count+1
        
        if(count>=self.majorityNum and self.log[N]==self.currentTerm):
            self.commitIndex=N
    
    def onRecAppendEntriesRPC(self, message):
        Receiver.onRecAppendEntriesRPC(message)
    
    def onRecReqVoteRPC(self, message):
        Receiver.onRecReqVoteRPC(message)
    
        
    
        