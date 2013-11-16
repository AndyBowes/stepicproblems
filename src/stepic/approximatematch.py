'''
Created on 16 Oct 2013

@author: Andy
'''
from suffixtree import Edge
from itertools import permutations, chain
from re import finditer, compile

def findApproximateMatches(motif, mismatches, dna):
    def applyWildCard(motif, pattern):
        if pattern == '1': return '.'
        return motif
    maskPattern = '1' * mismatches + '0' * (len(motif) - mismatches)
    patterns = ["".join(p) for p in set(permutations(maskPattern))]
    regexs = [ compile("".join(map(applyWildCard, motif, p))) for p in patterns]
    starts = list(set(chain.from_iterable([findRegexLocations(dna, regex) for regex in regexs])))
    return starts

def findMotifLocations(dna, motif):
    return findRegexLocations(dna, compile(motif))

def findRegexLocations(dna, regex):
    return [ match.start() for match in finditer(regex, dna)]
    
def buildKmerTree(dna, kmerLength):
    """
    Build a Suffix Tree which contains all of the Kmers in the DNA
    """
    root = Edge('')
    for i in range(len(dna)-kmerLength):#
        root.addEdge(dna[i:i+kmerLength]+'$', i)
    return root

if __name__ == '__main__':
#    tree = buildKmerTree('CGCCCGAATCCAGAACGCATTCCCATATTTCGGGACCACTGGCCTCCACGGTACGGACGTCAATCAAAT', 4)
    #tree.doWalk()
    #kmers = product(['A','C','G','T'], repeat=9)
    #print len(list(kmers))
    print " ".join([ str(s) for s in sorted(findApproximateMatches('ATTCTGGA', 3, 'CGCCCGAATCCAGAACGCATTCCCATATTTCGGGACCACTGGCCTCCACGGTACGGACGTCAATCAAAT'))])
