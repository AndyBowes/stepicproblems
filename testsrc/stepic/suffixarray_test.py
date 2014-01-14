# pylint: disable-msg=R0904
"""
Created on 13 Jan 2014

"""
import unittest

from stepic.suffixarray import buildSuffixArray

class Test(unittest.TestCase):

    def testBuildSuffixArray(self):
        with open('data/suffix/buildsuffixarray.txt') as fp:
            with open('data/suffix/buildsuffixarray.out', 'w') as output:
                sequences = [x.strip() for x in fp.readlines()]
#                output.write(', '.join([str(x) for x in buildSuffixArray(sequences[0])]))
                print buildSuffixArray(sequences[0])

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testBuildSuffixArray']
    unittest.main()
