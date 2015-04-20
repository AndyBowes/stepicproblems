'''
Created on 15 Apr 2015

@author: Andy
'''
import unittest
from stepic.phylogeny.ultrametric import findLowestElement

class UltrametricTest(unittest.TestCase):

    def testFindLowestElement(self):
        distanceMatrix = [[0,20,17,11],[20,0,20,13],[17,20,0,10],[11,13,10,0]]
        minPos = findLowestElement(distanceMatrix)
        self.assertIsNotNone(minPos)
        self.assertEqual((2,3), minPos)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()