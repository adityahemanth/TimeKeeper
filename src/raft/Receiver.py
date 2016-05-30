'''
Created on 25 May 2016

@author: Johnny
'''
from RequestVoteRPCReply import RequestVoteRPCReply
from AppendEntriesRPCReply import AppendEntriesRPCReply

class Receiver(object):
    
    def onRecReqVoteRPC(self, message):
        votedGranted=False
        return RequestVoteRPCReply(self.currentTerm,votedGranted,self.dc_ID)
    
    def onRecAppendEntriesRPC(self,message):
        success=False
        return AppendEntriesRPCReply(self.currentTerm,success,self.dc_ID,0)
    