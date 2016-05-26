from ServerState import ServerState
from Sender import Sender
from RequestVoteRPC import RequestVoteRPC
from Follower import Follower
from AppendEntriesRPCReply import AppendEntriesRPCReply
class Candidate(ServerState,Follower):
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
        self.votedFor=self.id
        self.receiverList[self.id]=False
        self.incrementVoteCount()
    def isMajorityGranted(self):
        if(self.voteCount>=self.majorityNum):
            return True
        else:
            return False
        
    def sendReqVoteRPC(self):
        lastLogIndex=len(self.log)-1
        lastLogTerm=self.log([lastLogIndex])
        
        reqRPC=RequestVoteRPC(self.term,self.id,lastLogIndex,lastLogTerm)
        
        for dcNum in range(self.numOfDC):
            if(self.receiverList[dcNum]):
                sender=Sender('RequestVoteRPC',reqRPC)
                sender.send(self.dc_list[dcNum])
    
    def onRecReqVoteRPCReply(self,message):
        if(message.term>self.term):
            self.setState('follower')
            return
        elif(message.term==self.term):
            if(message.voteGranted):
                self.receiverList[message.voterId]=False
                self.incrementVoteCount()
            else:
                pass
        else:
            pass
        
        if(self.isMajorityGranted()):
            self.setState('leader')
    
    def onRecReqVoteRPC(self, message):
        return Follower.onRecReqVoteRPC(self, message)
    
    def onRecAppendEntriesRPC(self,message):
        if(message.term>=self.term):
            self.setState('follower')
            return super(Candidate,self).onRecAppendEntriesRPC(message)
        else:
            success=False
            return AppendEntriesRPCReply(self.currentTerm,success)
    