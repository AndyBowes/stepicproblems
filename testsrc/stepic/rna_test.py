'''
Created on 24 Oct 2013

@author: root
'''
import unittest
from stepic.rna import cyclopeptideSequencing, linearSpectrum, sublist, cyclicSpectrum, \
                    leaderboardCyclopeptideSequencing, convolutionCyclopeptideSequencing, \
                    peptideEncoding, proteinTranslation

class Test(unittest.TestCase):

    def testProteinTranslation(self):
        with open('data/rna/proteinEncoding.txt') as fp:
            print proteinTranslation(fp.readline())

    def testPeptideEncoding(self):
        with open('data/rna/peptideEncoding.txt') as fp:
            dna = fp.readline().strip()
            protein = fp.readline().strip()
            for x in peptideEncoding(dna, protein):
                print x

    def getSpectrum(self):
        with open('data/cyclopeptidesequencing.txt') as fp:
            return [ int(x) for x in fp.readline().split()]


    def testCycloPeptideSequencing(self):
        with open('data/cyclopeptidesequencing.txt') as fp:
            with open('data/cyclopeptidesequencing.out', 'w') as out:
                spectrum = [ int(x) for x in fp.readline().split()]
                out.write(" ".join(list(set(cyclopeptideSequencing(spectrum)))))

    def testSpectrum(self):
        print ' '.join([str(m) for m in cyclicSpectrum('LLSLWAVFNNGD')])

    def testOccursCheck(self):
        spectrum = self.getSpectrum()
        for pep in [ 'QMAT', 'NAQ', 'TNA']:
            pepSpectrum = linearSpectrum(pep)
            print '{0} : {1}'.format(pep, ' '.join([str(x) for x in pepSpectrum]))
            print 'Sublist ' + str(sublist(pepSpectrum, spectrum))

    def testSpectrumsMatch(self):
        spectrum = self.getSpectrum()
        self.assertEquals(cyclicSpectrum('QMTNAQAN'), spectrum)

    @unittest.skip('Too long')
    def testLeaderBoardCyclopeptideSequencing(self):
        with open('data/leaderboardcyclopeptide2.txt') as fp:
            n = int(fp.readline().strip())
            spectrum = sorted([ int(x) for x in fp.readline().split()])
            print leaderboardCyclopeptideSequencing(spectrum, n)

    def testConvolutionCyclicSequence(self):
        with open('data/convolutionCyclicSequence.txt') as fp:
            m = int(fp.readline().strip())
            n = int(fp.readline().strip())
            spectrum = sorted([ int(x) for x in fp.readline().split()])
            print convolutionCyclopeptideSequencing(spectrum, m, n)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
