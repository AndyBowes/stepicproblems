# pylint: disable-msg=R0904
"""
Created on 11 Jan 2014

"""
import unittest

from stepic.suffixtree import suff, longestRepeat

class Test(unittest.TestCase):

    def testSuffixTree(self):
        with open('data/suffix/buildsuffixtree.txt') as fp:
            sequences = [x.strip() for x in fp.readlines()]
            suff(sequences[0])

    def testLongestRepeat(self):
        with open('data/suffix/longestrepeat.txt') as fp:
            sequences = [x.strip() for x in fp.readlines()]
            print longestRepeat(sequences[0] + '$')

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testSuffixTree']
    unittest.main()
