from StateController import StateController
from Sender import Sender
from AppendEntriesRPC import AppendEntriesRPC
from RequestVoteRPC import RequestVoteRPC
from Follower import Follower
from AppendEntriesRPCReply import AppendEntriesRPCReply
from Leader import Leader
from RequestVoteRPCReply import RequestVoteRPCReply
from Receiver import Receiver

class Candidate(StateController,Receiver):
    def reset(self):
        self.onPeriodEnd()
        self.setTimer()
        self.resetvoteCount()
        self.resetReceiverList()
        self.voteForSelf()
        self.incrementTerm()
    
    def resetvoteCount(self):
        self.voteCount=0
    def resetReceiverList(self):
        for dcNum in range(self.numOfDC):
            self.receiverList.append(True)
    
    def incrementVoteCount(self):
        self.voteCount=self.voteCount+1
    def incrementTerm(self):
        self.currentTerm=self.currentTerm+1
    def voteForSelf(self):
        self.votedFor=self.dc_ID
        self.receiverList[self.dc_ID]=False
        self.incrementVoteCount()
        
    def sendReqVoteRPC(self):
        lastLogIndex=self.log.getLastIndex()
        lastLogTerm=self.log.getLastTerm()
        
        reqRPC=RequestVoteRPC(self.term,self.dc_ID,lastLogIndex,lastLogTerm)
        
        for dcNum in range(self.numOfDC):
            if(self.receiverList[dcNum]):
                sender=Sender('RequestVoteRPC',reqRPC)
                sender.send(self.dc_list[dcNum])
    
    def onRecReqVoteRPCReply(self,message):
    
        if(message.term==self.term):
            if(message.voteGranted):
                self.receiverList[message.voterId]=False
                self.incrementVoteCount()
            else:
                pass
        elif(message.term<self.term):
            pass
        
        if(self.isMajorityGranted()):
            self.onMajorityGranted()
            
    def isMajorityGranted(self):
        if(self.voteCount>=self.majorityNum):
            return True
        else:
            return False
    
    def onMajorityGranted(self):
        self.setState('leader')
        StateController.reset()
    
    def onTimeout(self):
        StateController.reset()
    