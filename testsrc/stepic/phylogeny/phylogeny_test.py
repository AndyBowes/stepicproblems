'''
Created on 6 Apr 2015

@author: Andy
'''
from stepic.phylogeny.phylogeny import removeEntry
import unittest

class RemoveEntryTest(unittest.TestCase):

    def testRemoveMiddleEntry(self):
        """
        """
        distanceMatrix= [[1,2,3],[1,2,3],[1,2,3]]
        distanceMatrix = removeEntry(distanceMatrix,1)
        self.assertEqual(distanceMatrix, [[1,3], [1,3]])
        
    def testRemoveFirstEntry(self):
        """
        """
        distanceMatrix= [[1,2,3],[1,2,3],[1,2,3]]
        distanceMatrix = removeEntry(distanceMatrix,0)
        self.assertEqual(distanceMatrix, [[2,3], [2,3]])
        
    def testRemoveLastEntry(self):
        """
        """
        distanceMatrix= [[1,2,3],[1,2,3],[1,2,3]]
        distanceMatrix = removeEntry(distanceMatrix,2)
        self.assertEqual(distanceMatrix, [[1,2], [1,2]])
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()