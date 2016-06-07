'''
Created on 25 May 2016

@author: Johnny
'''

from LogItem import LogItem
from Post import Post

class Log(object):
    


    def __init__(self,numOfDc):
        
        self.log=[]
        
        self.versionNumList=[]
        for dcNum in range(numOfDc):
            self.versionNumList.append(0)
        
        self.log.append(LogItem(Post(0,0,0),0,0))
        self.posts=[]
        self.commitIndex=0
                
    def append(self,logItem):
        if(logItem==None):
            pass
        else:
            if(self.checkPost(logItem.post)):
                self.log.append(logItem)
                self.incrementVersionNumber(logItem.post)
                self.posts.append(logItem.post.post)
                
                #print('Appending new Entry: '+str(self.getLastIndex()));
                #self.display()
    def setLogItem(self,logItem,index):
        if(self.getLogItem(index)==None):            
            self.append(logItem)
                
    def setCommitIndex(self,commitIndex):
        self.commitIndex=commitIndex 
    
    def incrementVersionNumber(self,post):
        self.versionNumList[post.dc_Id]=post.versionNumber
    
    def checkPost(self,post):
        if(post.versionNumber>self.versionNumList[post.dc_Id]):
            return True;
        else:
            return False;   
    
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
        
        if(index>self.getLastIndex()):
            return None
        else:
            return self.log[index].term
    
    def getPost(self,index):
        
        if(index>self.getLastIndex()):
            return None
        else:
            return self.log[index].post.post
    
    
    def getLen(self):
        return len(self.log)
    
    def display(self):
        for index in range(self.getLen()):
            if(index>self.commitIndex):
                break
            if (index==0):
                continue
            print("Index: "+str(self.getIndex(index))+", Term: "+str(self.getTerm(index))+", Post: "+str(self.getPost(index)))
    
    def displayPosts(self):
        for index in range(self.getLen()):
            if(index>self.commitIndex):
                break
            if (index==0):
                continue
            print("Index: "+str(self.getIndex(index))+", Post: "+str(self.getPost(index)))
    
        