# pylint: disable-msg=R0904
"""
Created on 11 Jan 2014

"""
import unittest

from stepic.suffixtree import suff, longestRepeat, longestSharedRepeat, shortestUnsharedSeq

class Test(unittest.TestCase):

    def testSuffixTree(self):
        with open('data/suffix/buildsuffixtree.txt') as fp:
            sequences = [x.strip() for x in fp.readlines()]
            suff(sequences[0])

    def testLongestRepeat(self):
        with open('data/suffix/longestrepeat.txt') as fp:
            sequences = [x.strip() for x in fp.readlines()]
            print longestRepeat(sequences[0] + '$')

    def testLongestSharedSeq(self):
        with open('data/suffix/longestsharedseq.txt') as fp:
            sequences = [x.strip() for x in fp.readlines()]
            print longestSharedRepeat(sequences[0], sequences[1] + '$')

    def testShortestUnsharedSeq(self):
        with open('data/suffix/shortestunsharedseq.txt') as fp:
            sequences = [x.strip() for x in fp.readlines()]
            print shortestUnsharedSeq(sequences[0], sequences[1])

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testSuffixTree']
    unittest.main()
