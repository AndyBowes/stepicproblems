# pylint: disable-msg=R0904
"""
Created on 13 Jan 2014

"""
import unittest

from stepic.suffixarray import buildSuffixArray

class Test(unittest.TestCase):


    def testBuildSuffixArray(self):
        with open('data/suffix/buildsuffixarray.txt') as fp:
            sequences = [x.strip() for x in fp.readlines()]
            print ', '.join([str(x) for x, _ in buildSuffixArray(sequences[0] + '$')])

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testBuildSuffixArray']
    unittest.main()
