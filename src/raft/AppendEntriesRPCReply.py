class AppendEntriesRPCReply:
    
    def __init__(self,followerId,term,success,matchIndex):
        self.followerId=followerId
        self.term=term
        self.success=success
        self.matchIndex=matchIndex