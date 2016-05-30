from Sender import Sender
from AppendEntriesRPC import AppendEntriesRPC
from RequestVoteRPC import RequestVoteRPC
from AppendEntriesRPCReply import AppendEntriesRPCReply
from Leader import Leader
from RequestVoteRPCReply import RequestVoteRPCReply
from Receiver import Receiver
from State import State

class Candidate(State):
    
    @staticmethod
    def reset():
        
        Candidate.resetVoteCount()
        Candidate.resetReceiverList()
        Candidate.voteForSelf()
        Candidate.incrementTerm()
    @staticmethod
    def resetVoteCount():
        State.voteCount=0
    
    @staticmethod
    def resetReceiverList():
        State.receiverList=[]
        for dcNum in range(State.numOfDc):
            State.receiverList.append(True)
    
    @staticmethod
    def incrementVoteCount():
        State.voteCount=State.voteCount+1
    
    @staticmethod
    def incrementTerm():
        State.currentTerm=State.currentTerm+1
    
    @staticmethod
    def voteForSelf():
        State.votedFor=State.dc_ID
        State.receiverList[State.dc_ID]=False
        Candidate.incrementVoteCount()
    
    @staticmethod    
    def sendReqVoteRPC():
        lastLogIndex=State.log.getLastIndex()
        lastLogTerm=State.log.getLastTerm()
        
        reqRPC=RequestVoteRPC(State.currentTerm,State.dc_ID,lastLogIndex,lastLogTerm)
        
        for dcNum in range(State.numOfDc):
            if(State.receiverList[dcNum]):
                sender=Sender('RequestVoteRPC',reqRPC)
                sender.send(State.dc_list[dcNum])
    
    @staticmethod
    def onRecReqVoteRPCReply(message):
    
        if(message.term==State.currentTerm):
            if(message.voteGranted):
                State.receiverList[message.voterId]=False
                Candidate.incrementVoteCount()
            else:
                pass
        elif(message.term<State.currentTerm):
            pass
    
    @staticmethod        
    def isMajorityGranted():
        if(State.voteCount>=State.majorityNum):
            return True
        else:
            return False
    
    @staticmethod
    def onMajorityGranted():
        Candidate.setState('leader')
    
    @staticmethod
    def onTimeout():
        pass    