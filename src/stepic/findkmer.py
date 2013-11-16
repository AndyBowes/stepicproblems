'''
Created on 13 Oct 2013

@author: Andy
'''
from collections import defaultdict
import itertools

def findFrequentKmer(dna, kmerLength):
    kmerFreq = defaultdict(itertools.repeat(0).next)  
    for i in range(0,len(dna) - kmerLength):
        kmer = dna[i:i+kmerLength]
        kmerFreq[kmer] += 1
    maxFreq = max(kmerFreq.itervalues())
    return [ k for k,v in kmerFreq.iteritems() if v == maxFreq ]

def clumping(dna, kmerLength, windowLength ,threshold):
    kmerFreq = defaultdict(itertools.repeat(0).next)  
    for i in range(0,windowLength-kmerLength):
        kmer = dna[i:i+kmerLength]
        kmerFreq[kmer] += 1

    clump = set([k for k, v in kmerFreq.iteritems() if v >= threshold])
    j = 0
    for i in range(windowLength-kmerLength,len(dna)-kmerLength):
        kmer = dna[j:j+kmerLength]
        kmerFreq[kmer] -= 1
        j += 1
        kmer = dna[i:i+kmerLength]
        kmerFreq[kmer] += 1
        if kmerFreq[kmer] >= threshold:
            clump.add(kmer)
            
    return [c for c in clump]
    
    
