'''
Created on 25 May 2016

@author: Johnny
'''

from LogItem import LogItem

class Log(object):
    


    def __init__(self):
        self.log=[]
        self.append(LogItem('',0,0))
    
    def append(self,logItem):
        if(logItem==None):
            pass
        else:
            self.log.append(logItem)
    
    def getLastIndex(self):
        return self.log[len(self.log)-1].getIndex()
    
    def getLastTerm(self):
        return self.log[len(self.log)-1].getTerm()
    
    def deleteLogItem(self):
        del self.log[len(self.log)-1]
    
    def getLogItem(self,index):
        if(index>self.getLastIndex()):
            return None
        else: 
            return self.log[index]
    
    def getIndex(self,index):
        if(index>self.getLastIndex()):
            return None
        else:
            return self.log[index].index
    
    def getTerm(self,index):
        
        print(index)
        
        if(index>self.getLastIndex()):
            return None
        else:
            return self.log[index].term
    
    def getLen(self):
        return len(self.log)
        