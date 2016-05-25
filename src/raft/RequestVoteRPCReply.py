class RequestVoteRPCReply:
    
    def __init__(self,term,voterId,voteGranted):
        self.term=term
        self.voterId=voterId
        self.voteGranted=voteGranted
        