'''
Created on 20 Apr 2015

@author: Andy
'''
import unittest


class Test(unittest.TestCase):
    def testName(self):

        dic0 = {'A':2,'C':0,'G':3,'T':1}
        dic1 = {'A':1,'C':2,'G':1,'T':2}
        
        dic2 = {char : min(v if k==char else v+1 for k,v in dic0.iteritems()) 
                        + min(v if k==char else v+1 for k,v in dic1.iteritems()) for char in 'ACGT'}
            
        print(dic2)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()