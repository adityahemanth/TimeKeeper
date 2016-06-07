from Sender import Sender
from AppendEntriesRPC import AppendEntriesRPC
from RequestVoteRPC import RequestVoteRPC
from AppendEntriesRPCReply import AppendEntriesRPCReply
from Leader import Leader
from RequestVoteRPCReply import RequestVoteRPCReply
from Receiver import Receiver
from State import State
from Log import Log

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
        for dcNum in range(State.totalNumOfDc):
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
    def sendReqVoteRPC(dcNum):
        lastLogIndex=State.log.getLastIndex()
        lastLogTerm=State.log.getLastTerm()
        
        reqRPC=RequestVoteRPC(State.currentTerm,State.dc_ID,lastLogIndex,lastLogTerm)
        
        if(State.receiverList[dcNum]):
            #print("Send ReqVoteRPC to: "+str(dcNum))
            print("("+str(State.dc_ID)+","+State.state+","+str(State.currentTerm)+'): Send Request to datacenter '+str(dcNum)) 
            
            sender=Sender('RequestVoteRPC',reqRPC)
            sender.setConn(State.dc_list[dcNum])
            sender.start()            
            
    @staticmethod
    def onRecReqVoteRPCReply(message):
    
        if(message.term==State.currentTerm):
            if(message.voteGranted and State.receiverList[message.voterId]):
                Candidate.incrementVoteCount()
                print("("+str(State.dc_ID)+","+State.state+","+str(State.currentTerm)+'): Datacenter '+str(message.voterId)+' voted YES!'+'  Vote count: '+str(State.voteCount)) 
                
            State.receiverList[message.voterId]=False
            print(message.voterId)
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