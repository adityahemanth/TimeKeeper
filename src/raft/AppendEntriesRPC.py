import socket
class AppendEntriesRPC:
    
    def __init__(self,term,leaderId,prevLogIndex,prevLogTerm,entry,leaderCommit):
        self.term=term
        self.leaderId=leaderId
        self.prevLogIndex=prevLogIndex
        self.prevLogTerm=prevLogTerm
        self.entry=entry
        self.leaderCommit=leaderCommit