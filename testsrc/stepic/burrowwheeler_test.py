# pylint: disable-msg=R0904
"""
Created on 15 Jan 2014

"""
import unittest

from stepic.burrowwheeler import burrowWheelerTransform


class Test(unittest.TestCase):

    def testBurrowWheelerTransform(self):
        with open('data/burrow/transform.txt') as fp:
            sequences = [x.strip() for x in fp.readlines()]
            print burrowWheelerTransform(sequences[0])


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
