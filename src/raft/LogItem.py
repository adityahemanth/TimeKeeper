'''
Created on 25 May 2016

@author: Johnny
'''
class LogItem(object):
    def __init__(self,post,term,index):
        self.post=post
        self.term=term
        self.index=index
        
    def getTerm(self):
        return self.term
    
    def getIndex(self):
        return self.index
    
    def getPost(self):
        return self.post