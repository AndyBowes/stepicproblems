# pylint: disable-msg=R0904
"""
Created on 5 Jan 2014

"""
import unittest
from stepic.syntegy import greedySorting, countBreakpoints, syntegenyBlockConstruction, twoBreakDistance

class Test(unittest.TestCase):

    def testGreedySorting(self):
        greedySorting([-3, +4, +1, +5, -2])

    def testGreedySortingFromFile(self):
        with open('data/syntegy/greedySort.txt') as fp:
            line = fp.readline().strip()
            seq = [int(x) for x in line[1:-1].split(' ')]
            greedySorting(seq)

    def testCountBreakpoints(self):
        self.assertEqual(8, countBreakpoints([+3, +4, +5, -12, -8, -7, -6, +1, +2, +10, +9, -11, +13, +14]))

    def testCountBreakpointsFromFile(self):
        with open('data/syntegy/countBreakpoints.txt') as fp:
            line = fp.readline().strip()
            seq = [int(x) for x in line[1:-1].split(' ')]
            print countBreakpoints(seq)

    def test2BreakDistance(self):
        dist = twoBreakDistance([[1, 2, 3, 4, 5, 6]], [[+1, -3, -6, -5], [+2, -4]])
        self.assertEqual(dist, 3)

    def test2BreakDistanceFromFile(self):
        with open('data/syntegy/2breakdistance.txt') as fp:
            genome1 = [ [int(y) for y in x.split(' ')] for x in fp.readline().strip()[1:-1].split(')(')]
            genome2 = [ [int(y) for y in x.split(' ')] for x in fp.readline().strip()[1:-1].split(')(')]
            dist = twoBreakDistance(genome1, genome2)
            print dist

    def testSyntegenyBlockConstruction(self):
        pos = list(syntegenyBlockConstruction(3, 'AAACTCATC', 'TTTCAAATC'))
        self.assertEqual(4, len(pos))
        self.assertTrue((0, 0) in pos)
        self.assertTrue((0, 4) in pos)
        self.assertTrue((4, 2) in pos)
        self.assertTrue((6, 6) in pos)

    def testSyntegenyBlockConstructionFromFile(self):
        with open('data/syntegy/syntegenyBlocks.txt') as fp:
            kmerLength = int(fp.readline().strip())
            seq1 = fp.readline().strip()
            seq2 = fp.readline().strip()
            kmerPos = list(syntegenyBlockConstruction(kmerLength, seq1, seq2))
            for pos in kmerPos:
                print pos

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testGreedySort']
    unittest.main()
