from ServerState import ServerState
from AppendEntriesRPC import AppendEntriesRPC
from Sender import Sender
class Leader(ServerState):
    
    def resetNextIndex(self):
        for i in range(self.numOfDC):
            self.nextIndex[i]=len(self.log)
            self.matchIndex[i]=-1
    
    def heartbeat(self,dcNum):
        
        return AppendEntriesRPC(self.currentTerm,\
                                self.id,self.nextIndex[dcNum]-1,\
                                self.log[self.nextIndex[dcNum]-1],\
                                [],self.commitIndex)
    
    def entry(self,dcNum):
        
        return AppendEntriesRPC(self.currentTerm,\
                                self.id,self.nextIndex[dcNum]-1,\
                                self.log[self.nextIndex[dcNum]-1],\
                                self.log[self.nextIndex[dcNum]],\
                                self.commitIndex)
    
    def sendAppendEntriesRPC(self):
        
        for dcNum in range(self.numOfDC):
            if(self.isSelf(dcNum)):
                continue
            if(self.isMatched(dcNum)):
                sender=Sender('AppendEntriesRPC',self.entry(dcNum))
                sender.send(self.dc_list[dcNum])
            else:
                sender=Sender('AppendEntriesRPC',self.heartbeat(dcNum))
                sender.send(self.dc_list[dcNum])            
            
    def isSelf(self,dcNum):
        return (self.id==dcNum)
    
    def isMatched(self,dcNum):
        return (self.matchIndex[dcNum]!=-1)
    
    def onRecAppendEntriesRPCReply(self,message):
        ServerState.onRecMessage()
        
        if()
        
        
        