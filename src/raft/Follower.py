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
                    print("("+str(State.dc_ID)+","+State.state+","+str(State.currentTerm)+'): Voted for datacenter '+str(message.candidateId))
                    Follower.setTimer()
                else:
                    voteGranted=False
            elif(State.votedFor!=message.candidateId):
                voteGranted=False
        else:
            State.currentTerm=message.term
            if(Follower.isComplete(message)):
                voteGranted=True
                print("("+str(State.dc_ID)+","+State.state+","+str(State.currentTerm)+'): Voted for datacenter '+str(message.candidateId))
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
                matchIndex=message.prevLogIndex
                
                if(message.entry==None):
                    pass
                else:
                    print("("+str(State.dc_ID)+","+State.state+","+str(State.currentTerm)+'): Accepted entry '+str(message.entry.getIndex())+' from datacenter '+str(message.leaderId)) 
                
                if(message.prevLogIndex==State.log.getLastIndex()):
                    State.log.setLogItem(message.entry,message.prevLogIndex+1)
                    matchIndex=State.log.getLastIndex()
                
                success=True
                Follower.checkCommit(message)
            else:
                times=State.log.getLastIndex()-message.prevLogIndex+1
                print('Mismatched: '+str(State.log.getLastIndex())+" "+str(message.prevLogIndex))
                if(times>0):
                    for i in range(times):
                        print('delete!!!')
                        State.log.deleteLogItem()
                matchIndex=0
                success=False 
        
        #print("Match Index: "+str(matchIndex))
                     
        return AppendEntriesRPCReply(State.currentTerm,success,matchIndex,State.dc_ID)
    
    @staticmethod
    def isMatched(message):
        
        if(not Follower.eql(State.log.getTerm(message.prevLogIndex),message.prevLogTerm)):
            #print('MisMatch2: '+str(State.log.getTerm(message.prevLogIndex))+str(message.prevLogTerm))
            #print('MisMatch2: '+str(message.prevLogIndex)+str(message.prevLogTerm))
            return False
        else:
            #print('Match2: '+str(State.log.getTerm(message.prevLogIndex))+str(message.prevLogTerm))
            #print('Match2: '+str(message.prevLogIndex)+str(message.prevLogTerm))
            return True        
    
    @staticmethod
    def onTimeout():
        Follower.setState('candidate')
    
    @staticmethod
    def checkCommit(message):
        if(message.leaderCommit > State.commitIndex):
            if(State.commitIndex==min(message.leaderCommit, State.log.getLastIndex())):
                return;
            State.commitIndex =min(message.leaderCommit, State.log.getLastIndex())
            State.log.setCommitIndex(State.commitIndex)
            
            print("("+str(State.dc_ID)+","+State.state+","+str(State.currentTerm)+'): '+ "Entry "+str(State.commitIndex)+" commited: ")
            #State.log.display()