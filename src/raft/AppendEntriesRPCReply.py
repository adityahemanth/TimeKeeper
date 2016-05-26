class AppendEntriesRPCReply:
    
    def __init__(self,term,success,matchIndex,followerId):
        self.followerId=followerId
        self.term=term
        self.success=success
        self.matchIndex=matchIndex