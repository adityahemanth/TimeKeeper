class AppendEntriesRPCReply:
    
    def __init__(self,term,success):
        self.term=term
        self.success=success