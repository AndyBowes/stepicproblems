'''
Created on 19 Apr 2015

@author: Andy
'''
import unittest

from stepic.phylogeny.nearestneighbour import constructNearestNeighbourMatrix

class Test(unittest.TestCase):

    def testConstructNearestNeighbourMatrix(self):
        """
        Construct the nearest neighbour matrix from a distance matrix
        """
        distanceMatrix = [[0,13,21,22],[13,0,12,13],[21,12,0,13],[22,13,13,0]]
        nearestNeighbour = constructNearestNeighbourMatrix(distanceMatrix)
        self.assertEqual(nearestNeighbour,
                         [[0,-68,-60,-60],[-68,0,-60,-60],[-60,-60,0,-68],[-60,-60,-68,0]])
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testConstructNearestNeighbourMatrix']
    unittest.main()