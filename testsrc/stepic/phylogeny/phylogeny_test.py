'''
Created on 6 Apr 2015

@author: Andy
'''
from stepic.phylogeny.phylogeny import removeEntry, calculateLimbLength 
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
        
class LimbLengthTest(unittest.TestCase):
    
    def testCalculateLimbLength(self):
        distanceMatrix = [[0,20,9,11],[20,0,17,11],[9,17,0,8],[11,11,8,0]]
        print calculateLimbLength(1, distanceMatrix)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()