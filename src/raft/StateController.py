import random
from Follower import Follower
from Candidate import Candidate
from Leader import Leader
from Receiver import Receiver
from Datacenter import Datacenter
from Sender import Sender
from time import time
class StateController(Datacenter,Follower,Candidate,Leader,Receiver):
    
    def setState(self,state):
        self.state=state
        
    def setTimer(self):
        self.waitTime=self.timeUnit*random.random()+self.timeUnit
        self.start=time.time()
        
    def isTimeout(self,currentTime):
        if(self.eql(self.state,'leader')):
            return False
        
        elapse=self.currentTime-self.start
        return (elapse>=self.waitTime)
    
    def onTimeout(self):
        if(self.eql(self.state,'follower')):
            Follower.onTimeout(self)
        elif(self.eql(self.state,'candidate')):
            Candidate.onTimeout(self)
        else:
            pass
    
    def stepDown(self,message):
        if(message.term>self.currentTerm and (not self.eql(self.State,'follower'))):
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
    
    def onRecAppendEntriesRPC(self,message):
        if(self.eql(self.state,'follower')):
            reply=Follower.onRecAppendEntriesRPC(self, message)
        else:
            reply=Receiver.onRecAppendEntriesRPC(self, message)
        
        sender=Sender('AppendEntriesRPCReply',reply)
        sender.send(self.dc_list[message.leaderId])  
    
    def onRecReqVoteRPC(self,message):
        if(self.eql(self.state,'follower')):
            reply=Follower.onRecReqVoteRPC(self, message)
        else:
            reply=Receiver.onRecReqVoteRPC(self, message)
        
        sender=Sender('RequestVoteRPCReply',reply)
        sender.send(self.dc_list[message.candidateId])
    
    def onRecAppendEntriesRPCReply(self,message):
        Leader.onRecAppendEntriesRPCReply(self,message)  
    
    def onRecReqVoteRPCReply(self,message):
        Candidate.onRecReqVoteRPCReply(self,message)    
    
    def sendAppendEntriesRPC(self):
        Leader.sendAppendEntriesRPC(self)
    
    def sendReqVoteRPC(self):
        Candidate.sendReqVoteRPC(self)
    
    def eql(self,a,b):
        return (a==b)
    