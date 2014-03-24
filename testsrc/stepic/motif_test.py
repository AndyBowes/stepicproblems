'''
Created on 16 Nov 2013

@author: andy
'''
import unittest
from stepic.motif import motifEnumeration, medianString, probableKmer, greedyMotifSearch, \
     randomisedMotifSearch, gibbsSampling

class MotifTest(unittest.TestCase):

    @unittest.skip('skipped')
    def testMotifEnumeration(self):
        kmers = list(motifEnumeration(['ATTTGGC', 'TGCCTTA', 'CGGTATC', 'GAAAATT'], 3, 1))
        self.assertEqual(len(kmers), 4)
        self.assertTrue('ATA' in kmers, ' Should contain AAT')
        self.assertTrue('ATT' in kmers, ' Should contain ATT')
        self.assertTrue('GTT' in kmers, ' Should contain GTT')
        self.assertTrue('TTT' in kmers, ' Should contain TTT')

    @unittest.skip('skipped')
    def testMotifEnumerationFromFile(self):
        with open('data/motifEnumeration.txt') as fp:
            vals = [ int(x) for x in fp.readline().split()]
            k = vals[0]
            d = vals[1]
            dna = fp.readlines()
            kmers = list(motifEnumeration(dna, k, d))
            print ' '.join(kmers)

    @unittest.skip('skipped')
    def testMedianStringFromFile(self):
        with open('data/medianString.txt') as fp:
            vals = [ int(x) for x in fp.readline().split()]
            k = vals[0]
            dna = fp.readlines()
            print medianString(dna, k)

    def testProbableKmerFromFile(self):
        with open('data/probableKmer.txt') as fp:
            dna = fp.readline().strip()
            vals = [ int(x) for x in fp.readline().strip().split(' ')]
            k = vals[0]
            fp.readline()  # Ignore Base Title
            profile = [[float(x) for x in l.strip().split(' ') ]  for l in fp.readlines()]
            kmer, prob = probableKmer(dna, k, profile)
            print kmer

    @unittest.skip('skipped')
    def testGreedyMotifSearch(self):
        k = 3
        dna = ['GGCGTTCAGGCA', 'AAGAATCAGTCA', 'CAAGGAGTTCGC', 'CACGTCAATCAC', 'CAATAATATTCG']
        bestMotifs, _ = greedyMotifSearch(dna, k)
        self.assertEquals(bestMotifs, ['CAG', 'CAG', 'CAA', 'CAA', 'CAA'])

    @unittest.skip('skipped')
    def testGreedyMotifSearchFromFile(self):
        """
        Greedy Motif Search from file
        """
        with open('data/greedyMotif2.txt') as fp:
            vals = [int(x) for x in fp.readline().strip().split(' ')]
            k = vals[0]
            dna = [seq.strip() for seq in fp.readlines()]
            bestMotifs, _ = greedyMotifSearch(dna, k)
            print 'Best Motifs'
            for motif in bestMotifs:
                print motif

    @unittest.skip('skipped')
    def testGreedyMotifSearchWithPseudocount(self):
        k = 3
        dna = ['GGCGTTCAGGCA', 'AAGAATCAGTCA', 'CAAGGAGTTCGC', 'CACGTCAATCAC', 'CAATAATATTCG']
        bestMotifs, _ = greedyMotifSearch(dna, k, True)
        self.assertEquals(bestMotifs, ['TTC', 'ATC', 'TTC', 'ATC', 'TTC'])

    @unittest.skip('skipped')
    def testGreedyMotifSearchWithPseudocountFromFile(self):
        """
        Greedy Motif Search from file
        """
        with open('data/greedyMotifPseudocount.txt') as fp:
            vals = [int(x) for x in fp.readline().split()]
            k = vals[0]
            dna = [seq for seq in fp.readlines()]
            bestMotifs, _ = greedyMotifSearch(dna, k, True)
            print 'Best Motifs'
            for motif in bestMotifs:
                print motif

    @unittest.skip('skipped')
    def testRandomisedMotifSearchFromFile(self):
        """
        Randomised Motif Search from file
        """
        with open('data/randomisedMotifSearch2.txt') as fp:
            vals = [int(x.strip()) for x in fp.readline().split(' ')]
            k = vals[0]
            dna = [seq.strip() for seq in fp.readlines()]
            bestMotifs, bestScore = randomisedMotifSearch(dna, k, 1000)
            print 'Best Motifs'
            for motif in bestMotifs:
                print motif
            print bestScore

    @unittest.skip('skipped')
    def testGibbsSamplingFromFile(self):
        """
        Gibbs Sampling from file
        """
        with open('data/gibbsSampling.txt') as fp:
            vals = [int(x) for x in fp.readline().split()]
            k = vals[0]
            n = vals[2]
            dna = [seq.strip() for seq in fp.readlines()]
            bestMotifs, bestScore = gibbsSampling(dna, k, n, 40)
            print 'Best Motifs'
            for motif in bestMotifs:
                print motif
            print bestScore



if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
