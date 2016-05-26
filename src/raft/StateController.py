import random
from Follower import Follower
from Candidate import Candidate
from Leader import Leader
from Receiver import Receiver
from Datacenter import Datacenter
from Sender import Sender
from time import time
from RequestVoteRPCReply import RequestVoteRPCReply 
from RequestVoteRPC import RequestVoteRPC 
from AppendEntriesRPCReply import AppendEntriesRPCReply
from AppendEntriesRPC import AppendEntriesRPC

class StateController(Datacenter,Follower,Candidate,Leader,Receiver):
    
    def setState(self,state):
        self.state=state
    
    def setPeriod(self):
        self.periodTime=0.5*self.timeUnit
        self.periodStart=time.time()
    def periodEnd(self,currentTime):
        if(self.eql(self.state,'follower')):
            return False
        elapse=currentTime-self.periodStart
        return (elapse>=self.periodTime)
    def onPeriodEnd(self):
        if(self.eql(self.state,'leader')):
            self.sendAppendEntriesRPC()
        elif(self.eql(self.state,'candidate')):
            self.sendReqVoteRPC()
        self.setPeriod()
            
            
    def setTimer(self):
        self.waitTime=self.timeUnit*random.random()+self.timeUnit
        self.start=time.time()
    def isTimeout(self,currentTime):
        if(self.eql(self.state,'leader')):
            return False
        elapse=self.currentTime-self.start
        return (elapse>=self.waitTime)
    def onTimeout(self):
        print("("+str(self.dc_ID)+","+self.state+","+str(self.currentTerm)+'): Time out!')
        if(self.eql(self.state,'follower')):
            Follower.onTimeout(self)
            print("("+str(self.dc_ID)+","+self.state+","+str(self.currentTerm)+'): State Switch to Candidate')
        elif(self.eql(self.state,'candidate')):
            Candidate.onTimeout(self)
            print("("+str(self.dc_ID)+","+self.state+","+str(self.currentTerm)+'): Increment Term')
        else:
            pass
    
    
    def stepDown(self,message):
        if(message.term>self.currentTerm and (not self.eql(self.State,'follower'))):
            self.setState('follower')
            Follower.reset(message.term)
            print("("+str(self.dc_ID)+","+self.state+","+str(self.currentTerm)+'): Step down...State Switch to Follower')
            return True
        else:
            return False
    
    def reset(self):
        if(self.eql(self.state,'follower')):
            pass
        elif(self.eql(self.state,'candidate')):
            Candidate.reset(self)
        elif(self.eql(self.state,'leader')):
            print("("+str(self.dc_ID)+","+self.state+","+str(self.currentTerm)+'): State Switch to Leader')
            Leader.reset(self)
        else:
            print('Wrong Resetting!!!')    
    
    def onRecAppendEntriesRPC(self,message):
        print("("+str(self.dc_ID)+","+self.state+","+str(self.currentTerm)+'): Receive AppendEntriesRPC from datacenter '+\
              str(message.leaderId))
        
        if(self.eql(self.state,'follower')):
            reply=Follower.onRecAppendEntriesRPC(self, message)
        else:
            reply=Receiver.onRecAppendEntriesRPC(self, message)
        
        sender=Sender('AppendEntriesRPCReply',reply)
        sender.send(self.dc_list[message.leaderId])  
    
    def onRecReqVoteRPC(self,message):
        print("("+str(self.dc_ID)+","+self.state+","+str(self.currentTerm)+'): Receive ReqVoteRPC from datacenter '+\
              str(message.candidateId))
        
        if(self.eql(self.state,'follower')):
            reply=Follower.onRecReqVoteRPC(self, message)
        else:
            reply=Receiver.onRecReqVoteRPC(self, message)
        
        sender=Sender('RequestVoteRPCReply',reply)
        sender.send(self.dc_list[message.candidateId])
    
    def onRecAppendEntriesRPCReply(self,message):
        print("("+str(self.dc_ID)+","+self.state+","+str(self.currentTerm)+'): Receive AppendEntriesRPCReply from datacenter '+\
              str(message.followerId))
        
        Leader.onRecAppendEntriesRPCReply(self,message)  
    
    def onRecReqVoteRPCReply(self,message):
        print("("+str(self.dc_ID)+","+self.state+","+str(self.currentTerm)+'): Receive ReqVoteRPCReply from datacenter '+\
              str(message.voterId))
        
        Candidate.onRecReqVoteRPCReply(self,message)    
    
    def sendAppendEntriesRPC(self):
        print("("+str(self.dc_ID)+","+self.state+","+str(self.currentTerm)+'): Send AppendEntriesRPC')
        
        Leader.sendAppendEntriesRPC(self)
    
    def sendReqVoteRPC(self):
        print("("+str(self.dc_ID)+","+self.state+","+str(self.currentTerm)+'): Send ReqVoteRPC')
        
        Candidate.sendReqVoteRPC(self)
    
    def eql(self,a,b):
        return (a==b)
    