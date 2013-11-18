'''
Created on 16 Nov 2013

@author: andy
'''
import unittest
from stepic.motif import motifEnumeration, medianString, probableKmer, greedyMotifSearch

class MotifTest(unittest.TestCase):

    def testMotifEnumeration(self):
        kmers = list(motifEnumeration(['ATTTGGC', 'TGCCTTA', 'CGGTATC', 'GAAAATT'], 3, 1))
        self.assertEqual(len(kmers), 4)
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

    def testMedianStringFromFile(self):
        with open('data/medianString.txt') as fp:
            vals = [ int(x) for x in fp.readline().split()]
            k = vals[0]
            dna = fp.readlines()
            print medianString(dna, k)

    def testProbableKmerFromFile(self):
        with open('data/probableKmer.txt') as fp:
            dna = fp.readline()
            vals = [ int(x) for x in fp.readline().split()]
            k = vals[0]
            fp.readline()  # Ignore Base Title
            profile = [[float(x) for x in l.split() ]  for l in fp.readlines()]
            print probableKmer(dna, k, profile)

    def testGreedMotifSearch(self):
        k = 3
        dna = ['GGCGTTCAGGCA', 'AAGAATCAGTCA', 'CAAGGAGTTCGC', 'CACGTCAATCAC', 'CAATAATATTCG']
        bestMotifs = greedyMotifSearch(dna, k)
        self.assertEquals(bestMotifs, ['CAG', 'CAG', 'CAA', 'CAA', 'CAA'])



if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
