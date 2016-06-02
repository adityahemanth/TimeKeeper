'''
Created on 29 May 2016

@author: Johnny
'''

from State import State

class TestClass1(State):
    '''
    classdocs
    '''
    
    def init(self):
        self.currentTerm=1;
    def show(self):
        print('t1:'+str(self.currentTerm))
    
    def test(self):
        self.init()
        self.currentTerm=0
        self.unWrapState()