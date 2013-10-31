'''
Created on 24 Oct 2013

@author: root
'''
import unittest
from stepic.rna import cyclopeptideSequencing, linearSpectrum, peptideToMassChain, sublist, cyclicSpectrum, leaderboardCyclopeptideSequencing

class Test(unittest.TestCase):
    def getSpectrum(self):
        with open('data/cyclopeptidesequencing.txt') as fp:
            return [ int(x) for x in fp.readline().split()]


    def testCycloPeptideSequencing(self):
        with open('data/cyclopeptidesequencing.txt') as fp:
            with open('data/cyclopeptidesequencing.out','w') as out:
                spectrum = [ int(x) for x in fp.readline().split()]
                out.write(" ".join(list(set(cyclopeptideSequencing(spectrum)))))

    def testSpectrum(self):
        print ' '.join([str(m) for m in linearSpectrum('QMTNAQAN')])
    
    def testOccursCheck(self):
        spectrum = self.getSpectrum()
        for pep in [ 'QMAT', 'NAQ', 'TNA']:
            pepSpectrum = linearSpectrum(pep)
            print '{0} : {1}'.format(pep, ' '.join([str(x) for x in pepSpectrum]))
            print 'Sublist ' + str(sublist(pepSpectrum, spectrum))

    def testSpectrumsMatch(self):
        spectrum = self.getSpectrum()
        self.assertEquals(cyclicSpectrum('QMTNAQAN'), spectrum)
        
    def testLeaderBoardCyclopeptideSequencing(self):
        with open('data/leaderboardcyclopeptide.txt') as fp:
            n = int(fp.readline().strip())
            spectrum = [ int(x) for x in fp.readline().split()]
            print leaderboardCyclopeptideSequencing(spectrum, n)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()