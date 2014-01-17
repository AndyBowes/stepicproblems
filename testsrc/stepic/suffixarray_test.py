# pylint: disable-msg=R0904
"""
Created on 13 Jan 2014

"""
import unittest

from stepic.suffixarray import buildSuffixArray, getSuffixEdges

class Test(unittest.TestCase):

    def testBuildSuffixArray(self):
        with open('data/suffix/buildsuffixarray.txt') as fp:
            with open('data/suffix/buildsuffixarray.out', 'w') as output:
                sequences = [x.strip() for x in fp.readlines()]
#                output.write(', '.join([str(x) for x in buildSuffixArray(sequences[0])]))
                print buildSuffixArray(sequences[0])

    def testGetSuffixEdges(self):
        with open('data/suffix/generatesuffixedges.txt') as fp:
            with open('data/suffix/generatesuffixedges.out', 'w') as output:
                sequence = fp.readline().strip()
                suffixArray = [int(x) for x in fp.readline().strip().split(',')]
                lcp = [int(x) for x in fp.readline().strip().split(',')]
#                output.write(', '.join([str(x) for x in buildSuffixArray(sequences[0])]))
                for edge in getSuffixEdges(sequence, suffixArray, lcp):
                    print edge

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testBuildSuffixArray']
    unittest.main()
