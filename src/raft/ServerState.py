import random
from Follower import Follower
from Candidate import Candidate
from Leader import Leader
from Receiver import Receiver
class ServerState(Follower,Candidate,Leader,Receiver):
    
    def __init__(self,currentTerm,votedFor,log,commitIndex,lastApplied,state,id,numOfDC,majorityNum,timeUnit):
        self.currentTerm=currentTerm
        self.votedFor=votedFor
        self.log=log
        self.commitIndex=commitIndex
        self.lastApplied=lastApplied
        self.state=state
        self.id=id
        self.numOfDC=numOfDC
        self.majorityNum=majorityNum
        self.timeUnit=timeUnit
    
    def setCommitIndex(self,commitIndex):
        self.commitIndex=commitIndex
        
    def setLastApplied(self,lastApplied):
        self.lastApplied=lastApplied
    
    def setState(self,state):
        self.state=state
        
    def setTimer(self):
        self.waitTime=self.timeUnit*random.random()+self.timeUnit
        
    def stepDown(self,message):
        if(message.term>self.currentTerm):
            self.setState('follower')
            Follower.reset(message.term)
            return True
        else:
            return False
        
    def reset(self):
        if(self.eql(self.state,'follower')):
            pass
        elif(self.eql(self.state,'candidate')):
            Candidate.reset(self)
        elif(self.eql(self.state,'leader')):
            Leader.reset(self)
        else:
            print('Wrong Resetting!!!')    
    
    def onRecAppendEntriesRPC(self,type,message):
        if(self.eql(type,'follower')):
            Follower.onRecAppendEntriesRPC(self, message)
        else:
            Receiver.onRecAppendEntriesRPC(self, message)
    
    def onRecReqVoteRPC(self,type,message):
        if(self.eql(type,'follower')):
            Follower.onRecReqVoteRPC(self, message)
        else:
            Receiver.onRecReqVoteRPC(self, message)
    
    def onRecAppendEntriesRPCReply(self, message):
        Leader.onRecAppendEntriesRPCReply(self,message)  
    
    def onRecReqVoteRPCReply(self, message):
        Candidate.onRecReqVoteRPCReply(self,message)    
    
    def sendAppendEntriesRPC(self):
        Leader.sendAppendEntriesRPC(self)
    
    def sendReqVoteRPC(self):
        Candidate.sendReqVoteRPC(self)
    
    def eql(self,a,b):
        return (a==b)
    