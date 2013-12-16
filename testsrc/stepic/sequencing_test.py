# pylint: disable-msg=R0904
"""
Created on 11 Dec 2013

"""
import unittest
from stepic.sequencing import manhatten

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

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
