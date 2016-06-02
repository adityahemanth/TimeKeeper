'''
Created on 29 May 2016

@author: Johnny
'''

from State import State
from TestClass1 import TestClass1

class TestClass(State):
    '''
    classdocs
    ''' 
    def test(self):
        self.init()
        self.currentTerm=2
        self.unWrapState()
    
        self.wrapState(2,2,2,2,2,2)
        
        
def main():
    t1=TestClass1()
    t1.init()
    t1.show()
    
    t=TestClass()
    t.test()
    
    t1.test()
    t1.show()


if __name__ == '__main__':
    main()
            