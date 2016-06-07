'''
Created on 29 May 2016

@author: Johnny
'''
from math import ceil
from Log import Log
import random
import time

class State(object):
    '''
    classdocs
    '''
    
    @staticmethod
    def init(dc_ID,numOfDc,timeUnit,dc_list,host,port):
        
        #Datacenter Info and Config
        State.setDcId(int(dc_ID))
        State.setNumOfDc(int(numOfDc))
        State.setMajorityNum()
        State.setTimeUnit(float(timeUnit))
        State.setDcList(dc_list)
        State.setHost(host)
        State.setPort(port)
        
        #initialize State as 'follower'
        State.setState('follower')
        State.setCurrentTerm(int(1))
        State.setTimer()
        State.periodTime=[]
        State.periodStart=[]
        for dcNum in range(State.numOfDc):
            State.periodTime.append(0.0)
            State.periodStart.append(0.0)
            State.setPeriod(dcNum)
        
        #Fields for Candidate and Follower
        State.setVotedFor(dc_ID)
        State.setVoteCount(0)
        State.receiverList=[]
        
        #Fields for Leader
        State.nextIndex=[]
        State.matchSuccess=[]
        State.matchIndex=[]
        
        #Log and commit Info
        State.log=Log(State.numOfDc)
        State.setCommitIndex(0)
        State.setLastApplied(0)

    @staticmethod
    def setDcId(dc_ID):
        State.dc_ID=dc_ID
   
    @staticmethod
    def setNumOfDc(numOfDc):
        State.numOfDc=numOfDc
    
    @staticmethod
    def setDcList(dc_list):
        State.dc_list = dc_list
    
    @staticmethod
    def setHost(host):
        State.host=host
        
    @staticmethod
    def setPort(port):
        State.port=port
    
    @staticmethod
    def setMajorityNum():
        State.majorityNum=ceil(State.numOfDc*1.0/2.0)
    
    @staticmethod
    def setTimeUnit(timeUnit):
        State.timeUnit=timeUnit
    
    @staticmethod
    def setPeriodTime(periodTime):
        State.periodTime=periodTime
    
    @staticmethod
    def setPeriodStart(periodStart):
        State.periodStart=periodStart
    
    @staticmethod
    def setTimerTime(timerTime):
        State.timerTime=timerTime
    
    @staticmethod
    def setTimerStart(timerStart):
        State.timerStart=timerStart        
    
    @staticmethod
    def setState(state):
        State.state=state
    
    @staticmethod
    def setLog(log):
        State.log=log
    
    @staticmethod
    def setCommitIndex(commitIndex):
        State.commitIndex=commitIndex
    
    @staticmethod
    def setLastApplied(lastApplied):
        State.lastApplied=lastApplied
    
    @staticmethod
    def setVotedFor(votedFor):
        State.votedFor=votedFor
    
    @staticmethod
    def setCurrentTerm(term):
        State.currentTerm=term
    
    @staticmethod
    def setVoteCount(voteCount):
        State.voteCount=voteCount
    
    @staticmethod
    def setPeriod(dcNum):
        State.periodTime[dcNum]=0.2*State.timerTime
        State.periodStart[dcNum]=time.time()
    
    @staticmethod
    def setTimer():
        State.timerTime=State.timeUnit*random.random()+State.timeUnit
        State.timerStart=time.time()
    
    @staticmethod
    def eql(a,b):
        return (a==b)
    
#               
#     def unWrapState():
#         
#         State.setDcId(State.dc_ID)
#         State.setNumOfDc(State.numOfDc)
#         State.setMajorityNum()
#         State.setDcList(State.dc_list)
#         State.setTimeUnit(State.timeUnit)
#         
#         State.setState(State.state)
#         State.setCurrentTerm(State.currentTerm)
#         State.setVotedFor(State.votedFor)
#         
#         State.setLog(State.log)
#         State.setCommitIndex(State.commitIndex)
#         State.setLastApplied(State.lastApplied)
#         
#         State.setPeriodTime(State.periodTime)
#         State.setPeriodStart(State.periodStart)
#         State.setTimerTime(State.timerTime)
#         State.setTimerStart(State.timerStart)
#     
#     def wrapState(state,currentTerm,votedFor,log,commitIndex,lastApplied,\
#                   periodTime,periodStart,timerTime,timerStart):
#         
#         State.setState(state)
#         State.setCurrentTerm(currentTerm)
#         State.setVotedFor(votedFor)
#         
#         State.setLog(log)
#         State.setCommitIndex(commitIndex)
#         State.setLastApplied(lastApplied)
#         
#         State.setPeriodTime(periodTime)
#         State.setPeriodStart(periodStart)
#         State.setTimerTime(timerTime)
#         State.setTimerStart(timerStart)    
#     
#     