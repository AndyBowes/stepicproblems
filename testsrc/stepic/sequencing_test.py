# pylint: disable-msg=R0904
"""
Created on 11 Dec 2013

"""
import unittest
from collections import defaultdict
from stepic.sequencing import manhatten, longestPath, localAlignment, PAM250

class SequencingTest(unittest.TestCase):

    def testManhatten(self):
        self.assertEqual(34, manhatten(4, 4, [[1, 0, 2, 4, 3], [4, 6, 5, 2, 1], [4, 4, 5, 2, 1], [5, 6, 8, 5, 3]],
                                             [[3, 2, 4, 0], [3, 2, 4, 2], [0, 7, 3, 3], [3, 3, 0, 2], [1, 3, 2, 2]]))

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

    def testLocalAlignment(self):
        with open('data/sequencing/localAlignment.txt') as fp:
            seqs = [l.strip() for l in fp.readlines()]
            score, align1, align2 = localAlignment(seqs[0], seqs[1], PAM250)
            print score
            print align1
            print align2

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
