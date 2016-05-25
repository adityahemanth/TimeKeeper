import socket
class AppendEntriesRPC:
    
    def __init__(self,term,leaderId,prevLogIndex,prevLogTerm,entries,leaderCommit):
        self.term=term
        self.leaderId=leaderId
        self.prevLogIndex=prevLogIndex
        self.prevLogTerm=prevLogTerm
        self.entries=entries
        self.leaderCommit=leaderCommit