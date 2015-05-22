'''
Created on 30 Apr 2015

@author: Andy
'''
import unittest
from stepic.phylogeny.clustering import averagePosition, squaredErrorDistortion, findFurthestPoint

class ClusteringTest(unittest.TestCase):

    def testAveragePosition(self):
        points = [[1.50, 2.00, 5.00],[1.0,1.0,6.2]]
        self.assertEqual([1.25,1.50,5.60], averagePosition(points))


    def testSquaredErrorDistortion(self):
        
        points =  [[2, 6], [4, 9], [5, 7], [6, 5], [8, 3]] 
        centres = [[4, 5], [7, 4]]
        
        distortion = squaredErrorDistortion(centres, points)
        print distortion
        
    def testFarthestFirstTraversal(self):
        points =  [[2, 6], [4, 9], [5, 7], [6, 5], [8, 3]] 
        centres = [[4, 5], [7, 4]]
        
        distortion = findFurthestPoint(centres, points)
        print distortion
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()