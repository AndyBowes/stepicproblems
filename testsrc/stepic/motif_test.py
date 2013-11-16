'''
Created on 16 Nov 2013

@author: andy
'''
import unittest
from stepic.motif import motifEnumeration

class MotifTest(unittest.TestCase):

    def testMotifEnumeration(self):
        kmers = list(motifEnumeration(['ATTTGGC','TGCCTTA','CGGTATC','GAAAATT'], 3, 1))
        self.assertEqual(len(kmers),4)
        self.assertTrue('ATA' in kmers, ' Should contain AAT')
        self.assertTrue('ATT' in kmers, ' Should contain ATT')
        self.assertTrue('GTT' in kmers, ' Should contain GTT')
        self.assertTrue('TTT' in kmers, ' Should contain TTT')
        
    def testMotifEnumerationFromFile(self):
        with open('data/motifEnumeration.txt') as fp:
            vals = [ int(x) for x in fp.readline().split()]
            k = vals[0]
            d = vals[1]
            dna = fp.readlines()
            kmers = list(motifEnumeration(dna, k, d))
            print ' '.join(kmers)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()