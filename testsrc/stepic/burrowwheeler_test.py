# pylint: disable-msg=R0904
"""
Created on 15 Jan 2014

"""
import unittest
from cProfile import Profile

from stepic.burrowwheeler import burrowWheelerTransform, findPatterns, partialSuffixArray, \
                                 multiPatternMatching, patternMatchWithMismatches

from stepic.approximatematch import findApproximateMatches

class Test(unittest.TestCase):

    def testBurrowWheelerTransform(self):
        with open('data/burrow/transform.txt') as fp:
            sequences = [x.strip() for x in fp.readlines()]
            print burrowWheelerTransform(sequences[0])

    def testBwtMatching(self):
        with open('data/burrow/bwtmatching.txt') as fp:
            bwt = fp.readline().strip()
            patterns = fp.readline().strip().split(' ')
            print ' '.join([str(x) for x in findPatterns(bwt, patterns)])

    def testPartialSuffixArray(self):
        with open('data/burrow/partialSuffixArray.txt') as fp:
            sequence = fp.readline().strip()
            freq = int(fp.readline().strip())
            for i, v in partialSuffixArray(sequence, freq):
                print str(i) + ',' + str(v)

    def testMultiPatternMatching(self):
        with open('data/burrow/multiPatternMatch.txt') as fp:
            sequence = fp.readline().strip()
            patterns = [l.strip() for l in fp.readlines()]
            print ' '.join([str(pos) for pos in sorted(multiPatternMatching(sequence + '$', patterns))])

    def testPatternMatchWithMismatches(self):
        with open('data/burrow/mismatchPatternMatchLarge.txt') as fp:
            sequence = fp.readline().strip()
            patterns = fp.readline().strip().split(' ')
#            print 'Patterns : {0}'.format(len(patterns))
            mismatches = int(fp.readline().strip())
            # print ' '.join([str(pos) for pos in sorted(patternMatchWithMismatches(sequence, patterns, mismatches))])
            print len(patterns)
            i = 0
            for motif in patterns:
                print i
                findApproximateMatches(motif, mismatches, sequence)
                i += 1

if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.testPatternMatchWithMismatches']
    unittest.main()
