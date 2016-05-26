import random
class ServerState:
    
    def __init__(self,currentTerm,votedFor,log,commitIndex,lastApplied,state,id,numOfDC,majorityNum,timeUnit):
        self.currentTerm=currentTerm
        self.votedFor=votedFor
        self.log=log
        self.commitIndex=commitIndex
        self.lastApplied=lastApplied
        self.state=state
        self.id=id
        self.numOfDC=numOfDC
        self.majorityNum=majorityNum
        self.timeUnit=timeUnit
    
    def setCommitIndex(self,commitIndex):
        self.commitIndex=commitIndex
        
    def setLastApplied(self,lastApplied):
        self.lastApplied=lastApplied
    
    def setState(self,state):
        self.state=state
        
    def setTimer(self):
        self.waitTime=self.timeUnit*random.random()+self.timeUnit