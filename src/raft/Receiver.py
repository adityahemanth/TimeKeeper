'''
Created on 25 May 2016

@author: Johnny
'''
from RequestVoteRPCReply import RequestVoteRPCReply
from AppendEntriesRPCReply import AppendEntriesRPCReply
from State import State

class Receiver(object):
    
    @staticmethod
    def onRecReqVoteRPC(message):
        votedGranted=False
        return RequestVoteRPCReply(State.currentTerm,votedGranted,State.dc_ID)
    
    @staticmethod
    def onRecAppendEntriesRPC(message):
        success=False
        return AppendEntriesRPCReply(State.currentTerm,success,State.dc_ID,0)
    