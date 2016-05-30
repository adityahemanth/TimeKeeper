'''
Created on 29 May 2016

@author: Johnny
'''

from State import State

class TestClass(State):
    '''
    classdocs
    ''' 
    def test(self):
        self.init()
        self.unWrap()
        
        print(str(self.currentTerm))
        print(1)
        
def main():
    t=TestClass()
    t.test()
    print("2")
    
    if __name__ == '__main__':
        main()
            