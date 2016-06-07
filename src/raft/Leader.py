from State import State
from RequestVoteRPCReply import RequestVoteRPCReply 
from RequestVoteRPC import RequestVoteRPC 
from AppendEntriesRPCReply import AppendEntriesRPCReply
from AppendEntriesRPC import AppendEntriesRPC
from Sender import Sender
from Receiver import Receiver
from Log import Log

class Leader(State):
    
    @staticmethod
    def reset():
        Leader.resetNextIndex()
    
    @staticmethod    
    def resetNextIndex():
        State.nextIndex=[]
        State.matchSuccess=[] 
        for dcNum in range(State.numOfDc):
            State.nextIndex.append(State.log.getLastIndex()+1)
            State.matchSuccess.append(False)
            State.matchIndex.append(0)
    
    @staticmethod
    def decrementNextIndex(dcNum):
        if(Leader.eql(1,State.nextIndex[dcNum])):
            pass
        else:
            State.nextIndex[dcNum]=State.nextIndex[dcNum]-1
    
    @staticmethod
    def incrementNextIndex(dcNum):
        if(Leader.eql(State.log.getLastIndex()+1,State.nextIndex[dcNum])):
            pass
        else:
            State.nextIndex[dcNum]=State.nextIndex[dcNum]+1
    
    @staticmethod
    def setMatchSuccess(dcNum,success):
        State.matchSuccess[dcNum]=success
    
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
    def sendAppendEntriesRPC(dcNum):
        
        if(Leader.isSelf(dcNum)):
            return
        
        if(State.matchSuccess[dcNum]):
            #print("Send AppendEntriesRPC Entry"+str(State.nextIndex[dcNum])+" to: "+str(dcNum))
            sender=Sender('AppendEntriesRPC',Leader.entry(dcNum))
            sender.setConn(State.dc_list[dcNum])
            sender.start()            
            
        else:
            #print("Send AppendEntriesRPC Heartbeat"+str(State.nextIndex[dcNum])+" to: "+str(dcNum))
            sender=Sender('AppendEntriesRPC',Leader.heartbeat(dcNum))
            sender.setConn(State.dc_list[dcNum])
            sender.start()            
            
    @staticmethod        
    def isSelf(dcNum):
        return (State.dc_ID==dcNum)
    
    @staticmethod
    def onRecAppendEntriesRPCReply(message):
        
        if(not message.success):
            
            Leader.setMatchIndex(message.followerId, message.matchIndex)
            Leader.setMatchSuccess(message.followerId, False)
            Leader.decrementNextIndex(message.followerId)
            
            #print("Retry AppendEntriesRPC "+str(State.nextIndex[message.followerId])+" to: "+str(message.followerId))
            
            print("("+str(State.dc_ID)+","+State.state+","+str(State.currentTerm)+'): '+'Datacenter '+str(message.followerId)+' unmatched! '+'Retry Entry '+str(State.nextIndex[message.followerId])) 
            
            sender=Sender('AppendEntriesRPC',Leader.heartbeat(message.followerId))
            sender.setConn(State.dc_list[message.followerId])
            sender.start()            
            Leader.setPeriod(message.followerId)
        else:
            if(not State.matchSuccess[message.followerId]):
                #print('matched the case!!!!')
                pass      
            else:
                Leader.incrementNextIndex(message.followerId)
   
            if(message.matchIndex==State.matchIndex[message.followerId]):
                pass
            else:
                print("("+str(State.dc_ID)+","+State.state+","+str(State.currentTerm)+'): '+'Datacenter '+str(message.followerId)+' matched with Entry '+str(message.matchIndex)) 
            
            #print('matched')
            Leader.setMatchIndex(message.followerId,message.matchIndex)
            Leader.setMatchSuccess(message.followerId, True)
            
            if(message.matchIndex>State.commitIndex):
                Leader.checkCommit(message.matchIndex)
    
    @staticmethod
    def checkCommit(N):
        count=0
        for dcNum in range(State.numOfDc):
            if(State.matchIndex[dcNum]>=N or Leader.isSelf(dcNum)): 
                count=count+1
        
        if(count>=State.majorityNum and State.log.getTerm(N)==State.currentTerm):
            if(State.commitIndex==N):
                return
            State.commitIndex=N
            State.log.setCommitIndex(State.commitIndex)
            
            print("("+str(State.dc_ID)+","+State.state+","+str(State.currentTerm)+')')
            print(str(State.commitIndex)+" commited: ")
            #State.log.display()

    
        
    
        