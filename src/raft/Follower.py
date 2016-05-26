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
        
        return RequestVoteRPCReply(self.currentTerm,voteGranted,self.id)
    
    def isComplete(self,message):
        self.lastLogIndex=len(self.log)-1
        self.lastLogTerm=self.log[self.lastLogIndex]
        
        if(self.lastLogTerm>message.lastLogTerm or \
           ((self.lastLogTerm==message.lastLogTerm) and \
            (self.lastLogIndex>message.lastLogIndex))):
            return False
        else:
            return True
    
    def onRecAppendEntriesRPC(self,message):
        if(message.term<self.currentTerm):
            success=False
            matchIndex=-1
        else:
            self.currentTerm=message.term
            self.setTimer()
            if(self.isMatched(message)):
                self.log.append(message.entry)
                matchIndex=len(self.log)-1
                success=True
            else:
                times=len(self.log)-message.prevLogIndex
                if(times>0):
                    for i in range(times):
                        del self.log[len(self.log)-1]
                
                matchIndex=-1
                success=False 
                
        return AppendEntriesRPCReply(self.currentTerm,success,matchIndex,self.id)
            
    def isMatched(self,message):
        if(message.prevLogIndex>len(self.log)-1):
            return False
        elif(self.log[message.prevLogIndex]!=message.prevLogTerm):
            return False
        else:
            return True        
        
    def onTimeout(self):
        self.setState('candidate')
        self.setTimer()
        self.reset()
    