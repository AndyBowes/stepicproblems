# pylint: disable-msg=R0904
"""
Created on 15 Jan 2014

"""
import unittest
from cProfile import Profile
from itertools import groupby
from stepic.burrowwheeler import burrowWheelerTransform, findPatterns, partialSuffixArray, \
                                 multiPatternMatching, patternMatchWithMismatches, findPatternWithMismatches, \
                                 inverseBurrowWheelerTransform

class Test(unittest.TestCase):

    def testBurrowWheelerTransform(self):
        with open('data/burrow/transform.txt') as fp:
            sequences = [x.strip() for x in fp.readlines()]
            print burrowWheelerTransform(sequences[0])

    def testBurrowWheelerTransform2(self):
        print burrowWheelerTransform('GATTGCTTTT$')

    def testInverseBurrowWheelerTransform(self):
        with open('data/burrow/inverseTransform.txt') as fp:
            sequences = [x.strip() for x in fp.readlines()]
            print inverseBurrowWheelerTransform(sequences[0])

    def testInverseBurrowWheelerTransform2(self):
        print inverseBurrowWheelerTransform('G$CAGCTAGGG')

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
            mismatches = int(fp.readline().strip())
            print 'Sequence Length:{0}   Patterns:{1}  Mismatches:{2}'.format(len(sequence), len(patterns), mismatches)
            print 'Min Pattern Length:{0}'.format(min([len(p) for p in patterns]))
            print ' '.join([str(pos) for pos in sorted(findPatternWithMismatches(sequence, patterns, mismatches))])

    def testEcoliGenome(self):
        def encode(seq):
            return [(len(list(group)), name) for name, group in groupby(seq)]

        with open('data/burrow/ecoligenome.txt') as fp:
            sequence = fp.readline().strip()
            print "Transform"
            bwt = burrowWheelerTransform(sequence)
            print "Start Encoding"
            encoded = encode(bwt)
            # print encoded
            print len([(x, y) for x, y in encoded if x >= 10 ])


if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.testPatternMatchWithMismatches']
    unittest.main()
