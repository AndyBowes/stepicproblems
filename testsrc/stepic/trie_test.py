# pylint: disable-msg=R0904
"""
Created on 10 Jan 2014

"""
import unittest

from stepic.trie import buildTrie, findMatches

class Test(unittest.TestCase):

    def testBuildTrie(self):
        with open('data/trie/buildtrie.txt') as fp:
            sequences = [x.strip() for x in fp.readlines()]
            root = buildTrie(sequences)
            root.walkTree()

    def testFindMatches(self):
        with open('data/trie/findmatches.txt') as fp:
            sequences = [x.strip() for x in fp.readlines()]
            matches = findMatches(sequences[0], sequences[1:])
            print ' '.join([str(x) for match in matches for x in match ])



if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testBuildT']
    unittest.main()
