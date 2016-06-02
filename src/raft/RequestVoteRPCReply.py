class RequestVoteRPCReply:
    
    def __init__(self,term,voteGranted,voterId):
        self.term=term
        self.voterId=voterId
        self.voteGranted=voteGranted
        