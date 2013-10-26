'''
Created on 24 Oct 2013

@author: root
'''
import unittest
from stepic.rna import cyclopeptideSequencing

class Test(unittest.TestCase):

    def testCycloPeptideSequencing(self):
        with open('data/cyclopeptidesequencing.txt') as fp:
            with open('data/cyclopeptidesequencing.out','w') as out:
                spectrum = [ int(x) for x in fp.readline().split()]
                out.write(" ".join(cyclopeptideSequencing(spectrum)))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()