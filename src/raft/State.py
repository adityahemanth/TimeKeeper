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
    def init(dc_ID,numOfDc,timeUnit,dc_list):
        
        #Datacenter Info and Config
        State.setDcId(int(dc_ID))
        State.setNumOfDc(int(numOfDc))
        State.setMajorityNum()
        State.setTimeUnit(float(timeUnit))
        State.setDcList(dc_list)
        
        #initialize State as 'follower'
        State.setState('follower')
        State.setCurrentTerm(1)
        State.setPeriod()
        State.setTimer()
        
        #Fields for Candidate and Follower
        State.setVotedFor(dc_ID)
        State.setVoteCount(0)
        State.receiverList=[]
        
        #Fields for Leader
        State.nextIndex=[]
        State.matchIndex=[]
        
        #Log and commit Info
        State.log=Log()
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
        (State.host,State.port) = dc_list[State.dc_ID]
        State.port=int(State.port)
    
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
    def setPeriod():
        State.periodTime=0.5*State.timeUnit
        State.periodStart=time.time()
    
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