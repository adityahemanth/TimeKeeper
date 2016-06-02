class RequestVoteRPC:
    
    def __init__(self,term,candidateId,lastLogIndex,lastLogTerm):
        
        self.term=term
        self.candidateId=candidateId
        self.lastLogIndex=lastLogIndex
        self.lastLogTerm=lastLogTerm
    