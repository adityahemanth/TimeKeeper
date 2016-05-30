from State import State
from RequestVoteRPCReply import RequestVoteRPCReply 
from RequestVoteRPC import RequestVoteRPC 
from AppendEntriesRPCReply import AppendEntriesRPCReply
from AppendEntriesRPC import AppendEntriesRPC
from Sender import Sender
from Receiver import Receiver

class Leader(State):
    
    @staticmethod
    def reset():
        Leader.resetNextIndex()
    
    @staticmethod    
    def resetNextIndex():
        for dcNum in range(State.numOfDc):
            State.nextIndex[dcNum]=State.log.getLastIndex()+1
            State.matchIndex[dcNum]=0
    
    @staticmethod
    def decrementNextIndex(dcNum):
        State.nextIndex[dcNum]=State.nextIndex[dcNum]-1
    
    @staticmethod
    def incrementNextIndex(dcNum):
        State.nextIndex[dcNum]=State.nextIndex[dcNum]+1
    
    @staticmethod
    def setMatchIndex(dcNum,matchIndex):
        State.matchIndex[dcNum]=matchIndex
    
    @staticmethod
    def heartbeat(dcNum):
        
        return AppendEntriesRPC(State.currentTerm,\
                                State.dc_ID,State.nextIndex[dcNum]-1,\
                                State.log.getTerm(State.nextIndex[dcNum]-1),\
                                None,State.commitIndex)
    
    @staticmethod
    def entry(dcNum):
        
        return AppendEntriesRPC(State.currentTerm,\
                                State.dc_ID,State.nextIndex[dcNum]-1,\
                                State.log.getTerm(State.nextIndex[dcNum]-1),\
                                State.log.getLogItem(State.nextIndex[dcNum]),\
                                State.commitIndex)
    
    @staticmethod
    def sendAppendEntriesRPC():
        
        for dcNum in range(State.numOfDc):
            if(Leader.isSelf(dcNum)):
                continue
            if(State.matchIndex[dcNum]!=0):
                sender=Sender('AppendEntriesRPC',Leader.entry(dcNum))
                sender.send(State.dc_list[dcNum])
            else:
                sender=Sender('AppendEntriesRPC',Leader.heartbeat(dcNum))
                sender.send(State.dc_list[dcNum])            
    
    @staticmethod        
    def isSelf(dcNum):
        return (State.dc_ID==dcNum)
    
    @staticmethod
    def onRecAppendEntriesRPCReply(message):
        
        if(not message.success):
            Leader.decrementNextIndex(message.followerId)
            print("("+str(State.dc_ID)+","+State.state+","+str(State.currentTerm)+'): Retry AppendEntriesRPC to datacenter '+\
                  str(message.followerId))
            sender=Sender('AppendEntriesRPC',Leader.heartbeat(message.followerId))
            sender.send(State.dc_list[message.followerId])            
            Leader.setPeriod()
        else:
            Leader.setMatchIndex(message.followerId, message.matchIndex)
            Leader.incrementNextIndex(message.followerId)
            if(message.matchIndex>State.commitIndex):
                Leader.checkCommit(message.matchIndex)
    
    @staticmethod
    def checkCommit(N):
        count=0
        for dcNum in range(State.numOfDc):
            if(State.matchIndex[dcNum]>=N or Leader.isSelf(dcNum)): 
                count=count+1
        
        if(count>=State.majorityNum and State.log[N]==State.currentTerm):
            State.commitIndex=N
    
        
    
        