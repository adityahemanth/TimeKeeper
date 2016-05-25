from ServerState import ServerState
from RequestVoteRPCReply import RequestVoteRPCReply 
from RequestVoteRPC import RequestVoteRPC 
from AppendEntriesRPCReply import AppendEntriesRPCReply
from AppendEntriesRPC import AppendEntriesRPC
import random

class Follower(ServerState):
        
    def onRecReqVoteRPC(self,message):
        if (message.term<self.currentTerm):
            voteGranted=False
        elif(message.term==self.currentTerm):
            if(self.votedFor==None or self.votedFor==message.candidateId):
                if(self.isComplete(message)):
                    voteGranted=True
                else:
                    voteGranted=False
            elif(self.votedFor!=message.candidateId):
                voteGranted=False
        else:
            if(self.isComplete(message)):
                voteGranted=True
                self.currentTerm=message.term
            else:
                voteGranted=False
        
        return RequestVoteRPCReply(self.currentTerm,voteGranted)
    
    def isComplete(self,message):
        self.lastLogIndex=len(self.log)-1
        self.lastLogTerm=self.log[self.lastLogIndex]
        
        if(self.lastLogTerm>message.lastLogTerm or \
           ((self.lastLogTerm==message.lastLogTerm) and \
            (self.lastLogIndex>message.lastLogIndex))):
            return False
        else:
            self.votedFor=message.candidateId
            self.setTimer()
            return True
    
    def onRecAppendEntriesRPC(self,message):
        if (message.term<self.currentTerm):
            success=False
        elif(message.term==self.currentTerm):
            self.setTimer()
            success=self.isMatched(message)
        else:
            self.setTimer()
            self.currentTerm=message.term
            success=self.isMatched(message)
        
        return AppendEntriesRPCReply(self.currentTerm,success)
            
    def isMatched(self,message):
        if(message.prevLogIndex>len(self.log)-1):
            return False
        elif(self.log[message.prevLogIndex]!=message.prevLogTerm):
            times=len(self.log)-message.prevLogIndex
            for i in range(times):
                del self.log[len(self.log)-1] 
            return False
        else:
            for i in range(len(message.entries)):
                self.log.append(message.entries[i])
            
            if(message.leaderCommit>self.commitIndex):
                self.commitIndex=min(len(self.log)-1,message.leaderCommit)
            return True        
        
    def setTimer(self):
        self.waitTime=self.timeUnit*random.random()+self.timeUnit
    
    def 
       if(timeOut()): 
           self.setState('candidate')
    