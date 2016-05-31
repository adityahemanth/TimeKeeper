import random
from Follower import Follower
from Candidate import Candidate
from Leader import Leader
from time import time
from RequestVoteRPCReply import RequestVoteRPCReply 
from RequestVoteRPC import RequestVoteRPC 
from AppendEntriesRPCReply import AppendEntriesRPCReply
from AppendEntriesRPC import AppendEntriesRPC
from math import ceil
from Log import Log
from State import State
from Receiver import Receiver
from Sender import Sender



class StateController(State):
    

    def periodEnd(self,currentTime,dcNum):
        if(StateController.eql(State.state,'follower') or StateController.eql(dcNum, State.dc_ID)):
            return False
        elapse=currentTime-State.periodStart[dcNum]
        return (elapse>=State.periodTime[dcNum])
    def onPeriodEnd(self,dcNum):
        if(StateController.eql(dcNum,State.dc_ID)):
            return
        
        if(StateController.eql(State.state,'leader')):
            self.sendAppendEntriesRPC(dcNum)
        elif(StateController.eql(State.state,'candidate')):
            self.sendReqVoteRPC(dcNum)
        StateController.setPeriod(dcNum)
            
    def isTimeout(self,currentTime):
        if(StateController.eql(State.state,'leader')):
            return False
        elapse=currentTime-State.timerStart
        return (elapse>=State.timerTime)
    def onTimeout(self):
        #print("("+str(State.dc_ID)+","+State.state+","+str(State.currentTerm)+'): Time out!')
        if(StateController.eql(State.state,'follower')):
            Follower.onTimeout()
            print("("+str(State.dc_ID)+","+State.state+","+str(State.currentTerm)+'): State Switch to Candidate')
            self.reset()
        elif(StateController.eql(State.state,'candidate')):
            Candidate.onTimeout()
            print("("+str(State.dc_ID)+","+State.state+","+str(State.currentTerm)+'): Increment Term')
            self.reset()
        else:
            pass
    
    def stepDown(self,message):
        if(message.term>State.currentTerm and (not StateController.eql(State.state,'follower'))):
            StateController.setState('follower')
            #print("("+str(State.dc_ID)+","+State.state+","+str(State.currentTerm)+'): Resetting Follower')
            Follower.reset(message.term)
            StateController.setTimer()
            print("("+str(State.dc_ID)+","+State.state+","+str(State.currentTerm)+'): Step down...State Switch to Follower')
            return True
        else:
            return False
    
    def reset(self):
        if(StateController.eql(State.state,'follower')):
            pass
        elif(StateController.eql(State.state,'candidate')):
            #print("("+str(State.dc_ID)+","+State.state+","+str(State.currentTerm)+'): Resetting Candidate')
            Candidate.reset()
            for dcNum in range(State.dc_ID):
                self.onPeriodEnd(dcNum)
            StateController.setTimer()
            
        elif(StateController.eql(State.state,'leader')):
            #print("("+str(State.dc_ID)+","+State.state+","+str(State.currentTerm)+'): Resetting Leader')
            Leader.reset()
            for dcNum in range(State.dc_ID):
                self.onPeriodEnd(dcNum)
            StateController.setTimer()
            
        else: 
            print('Wrong Resetting!!!')    

    def onRecAppendEntriesRPC(self,message):
        print("("+str(State.dc_ID)+","+State.state+","+str(State.currentTerm)+'): Receive AppendEntriesRPC from: '+\
              str(message.leaderId)+" term"+str(message.term))
        
        if(StateController.eql(State.state,'follower')):
            reply=Follower.onRecAppendEntriesRPC(message)
        else:
            reply=Receiver.onRecAppendEntriesRPC(message)
        
        sender=Sender('AppendEntriesRPCReply',reply)
        sender.send(self.dc_list[message.leaderId])  
    
    def onRecReqVoteRPC(self,message):
        print("("+str(State.dc_ID)+","+State.state+","+str(State.currentTerm)+'): Receive ReqVoteRPC from: '+\
              str(message.candidateId)+" term"+str(message.term))
        
        if(StateController.eql(State.state,'follower')):
            reply=Follower.onRecReqVoteRPC(message)
        else:
            reply=Receiver.onRecReqVoteRPC(message)
        
        print(reply.voteGranted)
        sender=Sender('RequestVoteRPCReply',reply)
        sender.send(self.dc_list[message.candidateId])
    
    def onRecAppendEntriesRPCReply(self,message):
        print("("+str(State.dc_ID)+","+State.state+","+str(State.currentTerm)+'): Receive AppendEntriesRPCReply from: '+\
              str(message.followerId)+" "+str(message.success)+" "+str(message.matchIndex)+" term"+str(message.term))
        if(StateController.eql(State.state,'Leader')):
            Leader.onRecAppendEntriesRPCReply(message)
        else:
            pass  
    
    def onRecReqVoteRPCReply(self,message):
        print("("+str(State.dc_ID)+","+State.state+","+str(State.currentTerm)+'): Receive ReqVoteRPCReply from: '+\
              str(message.voterId)+" "+str(message.voteGranted)+" term"+str(message.term))
        
        if(StateController.eql(State.state,'candidate')):
            Candidate.onRecReqVoteRPCReply(message)
            if(self.isMajorityGranted()):
                self.onMajorityGranted()    
        else:
            pass
        
    def onMajorityGranted(self):
        Candidate.onMajorityGranted()
        self.reset()
    
    def isMajorityGranted(self):
        return Candidate.isMajorityGranted()
    
    def sendAppendEntriesRPC(self,dcNum):
        print("("+str(State.dc_ID)+","+State.state+","+str(State.currentTerm)+'): Send AppendEntriesRPC')
        
        Leader.sendAppendEntriesRPC(dcNum)
    
    def sendReqVoteRPC(self,dcNum):
        print("("+str(State.dc_ID)+","+State.state+","+str(State.currentTerm)+'): Send ReqVoteRPC')
        
        Candidate.sendReqVoteRPC(dcNum)
    