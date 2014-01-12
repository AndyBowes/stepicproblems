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
            buildTrie(sequences)

    def testFindMatches(self):
        with open('data/trie/findmatches.txt') as fp:
            sequences = [x.strip() for x in fp.readlines()]
            matches = findMatches(sequences[0], sequences[1:])
            for match in matches:
                if len(match) > 0:
                    print ' '.join([str(x) for x in match])



if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testBuildT']
    unittest.main()
