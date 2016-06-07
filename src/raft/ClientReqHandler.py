'''
Created on Jun 2, 2016

@author: Johnny
'''

from State import State
from Message import Message
from LogItem import LogItem
from Log import Log
import socket
import pickle

class ClientReqHandler(object):
    
    def onRecCreatePostReq(self,message,c):
        
        if(not State.eql(State.state,'leader')):
            c.send(pickle.dumps(False,0))
        else:
            logItem=LogItem(message,State.currentTerm,State.log.getLastIndex()+1)
            State.log.append(logItem)
            print("("+str(State.dc_ID)+","+State.state+","+str(State.currentTerm)+'): Received Create Post Request!')
            c.send(pickle.dumps(True,0))
            
    
    def onRecConfigChangeReq(self,message,c):
        
        print("("+str(State.dc_ID)+","+State.state+","+str(State.currentTerm)+'): Config changes!')
        State.configChange(message)
        c.send(pickle.dumps('Datacenter '+str(State.dc_ID)+' receives config changes!',0))