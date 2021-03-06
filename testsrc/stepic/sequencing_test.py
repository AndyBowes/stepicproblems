# pylint: disable-msg=R0904
"""
Created on 11 Dec 2013

"""
import unittest
from collections import defaultdict
from stepic.sequencing import manhatten, longestPath, localAlignment, globalAlignment, PAM250, editDistance, \
                fittingAlignment, overlapAlignment, affineAlignment, findMiddleEdge, multipleSequenceAlignment, \
                BLOSUM62, longestCommonSubsequence

class SequencingTest(unittest.TestCase):

    @unittest.skip('')
    def testManhatten(self):
        self.assertEqual(34, manhatten(4, 4, [[1, 0, 2, 4, 3], [4, 6, 5, 2, 1], [4, 4, 5, 2, 1], [5, 6, 8, 5, 3]],
                                             [[3, 2, 4, 0], [3, 2, 4, 2], [0, 7, 3, 3], [3, 3, 0, 2], [1, 3, 2, 2]]))

    @unittest.skip('')
    def testManhattenFromFile(self):
        with open('data/sequencing/manhatten.txt') as fp:
            n = int(fp.readline().strip())
            m = int(fp.readline().strip())
            down = []
            for i in range(n):
                down.append([int(x) for x in fp.readline().strip().split()])
            right = []
            fp.readline()
            for i in range(n + 1):
                right.append([int(x) for x in fp.readline().strip().split()])
            self.assertEqual(85, manhatten(m, n, down, right))

    @unittest.skip('')
    def testLongestPath(self):
        with open('data/sequencing/longestdag.txt') as fp:
            start = int(fp.readline().strip())
            finish = int(fp.readline().strip())
            nodes = defaultdict(list)
            for line in fp.readlines():
                elements = line.split('->')
                values = [int(x) for x in elements[1].split(':')]
                nodes[int(elements[0])].append((values[0], values[1]))
            maxLength, path = longestPath(start, finish, nodes)
            print maxLength
            print '->'.join([str(x) for x in path])

    @unittest.skip('')
    def testLocalAlignment(self):
        with open('data/sequencing/localAlignment.txt') as fp:
            seqs = [l.strip() for l in fp.readlines()]
            score, align1, align2 = localAlignment(seqs[0], seqs[1], PAM250)
            print score
            print align1
            print align2

#     def testGlobalAlignment(self):
#         with open('data/sequencing/globalAlignment.txt') as fp:
#             seqs = [l.strip() for l in fp.readlines()]
#             score, align1, align2 = globalAlignment(seqs[0], seqs[1], BLOSUM62)
#             print score
#             print align1
#             print align2

    @unittest.skip('')
    def testLongestCommonSubsequence(self):
        with open('data/sequencing/longestCommonSubsequence.txt') as fp:
            seqs = [l.strip() for l in fp.readlines()]
            subseq = longestCommonSubsequence(seqs[0], seqs[1])
            print subseq


    @unittest.skip('')
    def testEditDistance(self):
        self.assertEqual(5, editDistance('PLEASANTLY', 'MEANLY'))

    @unittest.skip('')
    def testEditDistanceFromFile(self):
        with open('data/sequencing/editDistance.txt') as fp:
            seqs = [l.strip() for l in fp.readlines()]
            print editDistance(seqs[0], seqs[1])

    @unittest.skip('')
    def testFittingAlignment(self):
        score, align1, align2 = fittingAlignment('GTAGGCTTAAGGTTA', 'TAGATA')
        self.assertEqual(2, score)
        self.assertEqual('TAGGCTTA', align1)
        self.assertEqual('TAGA--TA', align2)

    @unittest.skip('')
    def testFittingAlignmentFromFile(self):
        with open('data/sequencing/fittingAlignment.txt') as fp:
            seqs = [l.strip() for l in fp.readlines()]
            score, align1, align2 = fittingAlignment(seqs[0], seqs[1])
            print score
            print align1
            print align2

    @unittest.skip('')
    def testOverlapAlignment(self):
        score, align1, align2 = overlapAlignment('PAWHEAE', 'HEAGAWGHEE')
        self.assertEqual(1, score)
        self.assertEqual('PAWHEAE------', align1)
        self.assertEqual('---HEAGAWGHEE', align2)

    @unittest.skip('')
    def testOverlapAlignmentFromFile(self):
        with open('data/sequencing/overlapAlignment.txt') as fp:
            seqs = [l.strip() for l in fp.readlines()]
            score, align1, align2 = overlapAlignment(seqs[0], seqs[1])
            print score
            print align1
            print align2

    @unittest.skip('')
    def testFindMiddleEdge(self):
        with open('data/sequencing/findMiddleEdge.txt') as fp:
            seqs = [l.strip() for l in fp.readlines()]
            print findMiddleEdge(seqs[0], seqs[1])

    def testAffineAlignmentFromFile(self):
        with open('data/sequencing/affineAlignment.txt') as fp:
            seqs = [l.strip() for l in fp.readlines()]
            score, align1, align2 = affineAlignment(seqs[0], seqs[1])
            print score
            print align1
            print align2

    @unittest.skip('')
    def testLinearAlignmentFromFile(self):
        with open('data/sequencing/linearAlignment.txt') as fp:
            seqs = [l.strip() for l in fp.readlines()]
            score, align1, align2 = affineAlignment(seqs[0], seqs[1], 5, 5)
            print score
            print align1
            print align2

    @unittest.skip('')
    def testMultipleAlignmentFromFile(self):
        with open('data/sequencing/multipleAlignment.txt') as fp:
            seqs = [l.strip() for l in fp.readlines()]
            score, align1, align2, align3 = multipleSequenceAlignment(seqs[0], seqs[1], seqs[2])
            print score
            print align1
            print align2
            print align3


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
