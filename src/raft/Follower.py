from RequestVoteRPCReply import RequestVoteRPCReply 
from RequestVoteRPC import RequestVoteRPC 
from AppendEntriesRPCReply import AppendEntriesRPCReply
from AppendEntriesRPC import AppendEntriesRPC
import random
from State import State
from Log import Log

class Follower(State):
    
    @staticmethod
    def reset(term):
        
        Follower.setCurrentTerm(term)
        Follower.resetVotedFor()
    
    @staticmethod
    def resetVotedFor():
        State.votedFor=None
    
    @staticmethod
    def onRecReqVoteRPC(message):
        
        if (message.term<State.currentTerm):
            voteGranted=False
        elif(message.term==State.currentTerm):
            if(State.votedFor==None or State.votedFor==message.candidateId):
                if(Follower.isComplete(message)):
                    voteGranted=True
                    State.votedFor=message.candidateId
                    Follower.setTimer()
                else:
                    voteGranted=False
            elif(State.votedFor!=message.candidateId):
                voteGranted=False
        else:
            State.currentTerm=message.term
            if(Follower.isComplete(message)):
                voteGranted=True
                State.votedFor=message.candidateId
                Follower.setTimer()
            else:
                State.votedFor=None
                voteGranted=False
        
        return RequestVoteRPCReply(State.currentTerm,voteGranted,State.dc_ID)
    
    @staticmethod
    def isComplete(message):
        
        lastLogIndex=State.log.getLastIndex()
        lastLogTerm=State.log.getLastTerm()
        
        if(lastLogTerm>message.lastLogTerm or \
           ((lastLogTerm==message.lastLogTerm) and \
            (lastLogIndex>message.lastLogIndex))):
            return False
        else:
            return True
    
    @staticmethod
    def onRecAppendEntriesRPC(message):
        
        if(message.term<State.currentTerm):
            success=False
            matchIndex=0
        else:
            State.currentTerm=message.term
            Follower.setTimer()
            if(Follower.isMatched(message)):
                State.log.append(message.entry)
                matchIndex=State.log.getLastIndex()
                success=True
            else:
                times=State.log.getLastIndex()-message.prevLogIndex+1
                if(times>0):
                    for i in range(times):
                        State.log.deleteLogItem()
                
                matchIndex=0
                success=False 
        
        print("Match Index: "+str(matchIndex))
                     
        return AppendEntriesRPCReply(State.currentTerm,success,matchIndex,State.dc_ID)
    
    @staticmethod
    def isMatched(message):
        if(message.prevLogIndex>State.log.getLastIndex()):
            return False
        elif(not Follower.eql(State.log.getTerm(message.prevLogIndex),message.prevLogTerm)):
            return False
        else:
            return True        
    
    @staticmethod
    def onTimeout():
        Follower.setState('candidate')
    
    