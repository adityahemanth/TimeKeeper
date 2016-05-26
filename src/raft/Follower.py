from StateController import StateController
from RequestVoteRPCReply import RequestVoteRPCReply 
from RequestVoteRPC import RequestVoteRPC 
from AppendEntriesRPCReply import AppendEntriesRPCReply
from AppendEntriesRPC import AppendEntriesRPC
import random
from Candidate import Candidate

class Follower(StateController,Candidate):
    
    def reset(self,term):
        self.setTimer()
        self.currentTerm=term
        self.resetVotedFor()
        
    def resetVotedFor(self):
        self.votedFor=None
    
    def onRecReqVoteRPC(self,message):
        if (message.term<self.currentTerm):
            voteGranted=False
        elif(message.term==self.currentTerm):
            if(self.votedFor==None or self.votedFor==message.candidateId):
                if(self.isComplete(message)):
                    voteGranted=True
                    self.votedFor=message.candidateId
                    self.setTimer()
                else:
                    voteGranted=False
            elif(self.votedFor!=message.candidateId):
                voteGranted=False
        else:
            self.currentTerm=message.term
            if(self.isComplete(message)):
                voteGranted=True
                self.votedFor=message.candidateId
                self.setTimer()
            else:
                self.votedFor=None
                voteGranted=False
        
        return RequestVoteRPCReply(self.currentTerm,voteGranted,self.dc_ID)
    
    def isComplete(self,message):
        self.lastLogIndex=self.log.getLastIndex()
        self.lastLogTerm=self.log.getLastTerm()
        
        if(self.lastLogTerm>message.lastLogTerm or \
           ((self.lastLogTerm==message.lastLogTerm) and \
            (self.lastLogIndex>message.lastLogIndex))):
            return False
        else:
            return True
    
    def onRecAppendEntriesRPC(self,message):
        if(message.term<self.currentTerm):
            success=False
            matchIndex=0
        else:
            self.currentTerm=message.term
            self.setTimer()
            if(self.isMatched(message)):
                self.log.append(message.entry)
                matchIndex=self.log.getLastIndex()
                success=True
            else:
                times=self.log.getLastIndex()-message.prevLogIndex+1
                if(times>0):
                    for i in range(times):
                        self.log.deleteLogItem()
                
                matchIndex=0
                success=False 
                
        return AppendEntriesRPCReply(self.currentTerm,success,matchIndex,self.dc_ID)
            
    def isMatched(self,message):
        if(message.prevLogIndex>self.log.getLastIndex()):
            return False
        elif(not self.eql(self.log.getTerm(message.prevLogIndex),message.prevLogTerm)):
            return False
        else:
            return True        
        
    def onTimeout(self):
        self.setState('candidate')
        StateController.reset()
    
    