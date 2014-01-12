'''
Created on 16 Nov 2013

@author: Andy Bowes
'''
from itertools import permutations, product, takewhile
from copy import copy
from random import randint, random

def getKmers(dna, k):
    """
    Find all the K-mers in a DNA sequence
    """
    for i in range(len(dna) - k + 1):
        yield dna[i:i + k]

def getKmerVariations(kmer, d):
    """
    Find all the possible variations on a kmer with at most d differences
    """
    def applyWildCard(char, pattern):
        if pattern == '1':
            return ['A', 'C', 'G', 'T']
        return [char]
    maskPattern = '1' * d + '0' * (len(kmer) - d)
    patterns = ["".join(p) for p in set(permutations(maskPattern))]
    variations = [''.join(k) for p in patterns for k in product(*map(applyWildCard, kmer, p))]
    return variations

def motifEnumeration(dna, k, d):
    """
    Enumerate the kmers with up to d differences
    """
    kmers = set([kmer for seq in dna for kmer in getKmers(seq, k) ])
    variants = sorted(set([v for kmer in kmers for v in getKmerVariations(kmer, d)]))
    for v in variants:
        v2 = getKmerVariations(v, d)
        for seq in dna:
            if not any([x in seq for x in v2]):
                break
        else:
            yield v

def hammingDistance(seq1, seq2):
    """
    Calculate the Hamming Distance between 2 Sequences
    """
    def checkChar(char1, char2):
        if char1 == char2:
            return 0
        return 1
    return sum([x for x in map(checkChar, seq1, seq2)])

def bestScore(dna, kmer):
    """
    Find the minimum Hamming Distance for a kmer in a DNA Sequence
    """
    return min([ hammingDistance(kmer, sub) for sub in getKmers(dna, len(kmer))])

def medianString(dna, k):
    """
    Find the Median String in a list of DNA Sequences
    This is the kmer with the lowest minimum Hamming Distance
    """
    kmers = ["".join(p) for p in product('ACGT', repeat=k)]
    bestKmer = 'A' * k
    topScore = 200000
    for kmer in kmers:
        score = sum([bestScore(seq, kmer) for seq in dna])
        if score <= topScore:
            topScore = score
            bestKmer = kmer
    return bestKmer

def kmerProb(kmer, profile):
    """
    Calculate the probability of a kmer given a Probility Profile
    """
    prob = 1.0
    for i in range(len(kmer)):
        prob *= profile[i]['ACGT'.index(kmer[i])]
    return prob

def probableKmer(dna, k, profile):
    """
    Find the most probable kmer in a dna sequence given a probability profile
    """
    kmers = getKmers(dna, k)
    bestKmer = ''
    bestProb = -1
    for kmer in kmers:
        prob = kmerProb(kmer, profile)
        if prob > bestProb:
            bestProb = prob
            bestKmer = kmer
    return bestKmer, bestProb

def scoreMotifs(motifs):
    """
    Calculate the Score for the supplied motifs
    """
    occurs = [[0 for _ in xrange(4)] for _ in xrange(len(motifs[0]))]
    noOfMotifs = len(motifs)
    for i in range(noOfMotifs):
        motif = motifs[i]
        for j in range(len(motif)):
            try:
                occurs[j]['ACGT'.index(motif[j])] += 1
            except IndexError as e:
                raise e
    return sum([noOfMotifs - max([x for x in m]) for m in occurs ])

def constructProbabilityProfile(motifs, pseudocount=False):
    """
    Construct the probability matrix for the set of Motifs
    """
    noOfMotifs = len(motifs) + 4 if pseudocount else len(motifs)
    defaultValue = 1.0 / noOfMotifs if pseudocount else 0.0
    occurs = [[defaultValue for _ in xrange(4)] for _ in xrange(len(motifs[0]))]
    for i in range(len(motifs)):
        motif = motifs[i]
        for j in range(len(motif)):
            occurs[j]['ACGT'.index(motif[j])] += (1.0 / noOfMotifs)
    return occurs

def greedyMotifSearch(dna, k, pseudocount=False):
    """
    Perform a Greedy Search for the best kmers on a set of DNA
    """
    motifs = [seq[:k] for seq in dna]
    bestMotifs = copy(motifs)
    motifScore = scoreMotifs(motifs)
    for i in range(len(dna[0]) - k):
        motifs[0] = dna[0][i:i + k]
        for j in range(1, len(dna)):
            profile = constructProbabilityProfile(motifs[:j], pseudocount)
            motifs[j], _ = probableKmer(dna[j], k, profile)
        score = scoreMotifs(motifs)
        if score < motifScore:
            motifScore = score
            bestMotifs = copy(motifs)
    return bestMotifs, motifScore

def randomisedMotifSearch(dna, k, t):
    """
    Perform a Search stating with a random set of Motifs
    """
    def doSearch(dna, k):
        motifs = [ '' for _ in range(len(dna))]
        for i in xrange(len(dna)):
            startPos = randint(0, len(dna[i]) - k)
            motifs[i] = dna[i][startPos:startPos + k]
        bestMotifs = copy(motifs)
        motifScore = scoreMotifs(motifs)
        while True:
            profile = constructProbabilityProfile(motifs, True)
            for j in range(len(dna)):
                motifs[j], _ = probableKmer(dna[j], k, profile)
            score = scoreMotifs(motifs)
            if score < motifScore:
                motifScore = score
                bestMotifs = copy(motifs)
            else:
                break
        return bestMotifs, motifScore
    recordMotifs = []
    recordScore = 10000
    for _ in range(t):
        iterMotifs, iterScore = doSearch(dna, k)
        if iterScore < recordScore:
            recordScore = iterScore
            recordMotifs = iterMotifs
    return recordMotifs, recordScore

def gibbsSampling(dna, k, n, t):
    """
    Perform a Gibbs Sampling Search stating with a random set of Motifs
    """
    def randomKmer(seq, k, profile):
        """
        Given a seq pick a random kmer based on the probability profile 
        """
        kmerProbs = [(kmer, kmerProb(kmer, profile))  for kmer in getKmers(seq, k)]
        totalProbability = sum([prob for _, prob in kmerProbs])
        randValue = random() * totalProbability
        for kp in kmerProbs:
            randValue -= kp[1]
            if randValue <= 0.0:
                return kp[0]

    def doSearch(dna, k, n):
        motifs = [ '' for _ in range(len(dna))]
        for i in xrange(len(dna)):
            startPos = randint(0, len(dna[i]) - k)
            motifs[i] = dna[i][startPos:startPos + k]
        bestMotifs = copy(motifs)
        motifScore = scoreMotifs(motifs)
        for _ in xrange(n):
            i = randint(0, len(motifs) - 1)
            profileMotifs = copy(motifs)
            profileMotifs.pop(i)
            profile = constructProbabilityProfile(profileMotifs, True)
            motifs[i] = randomKmer(dna[i], k, profile)
            score = scoreMotifs(motifs)
            if score < motifScore:
                motifScore = score
                bestMotifs = copy(motifs)
        return bestMotifs, motifScore
    recordMotifs = []
    recordScore = 10000
    for _ in range(t):
        iterMotifs, iterScore = doSearch(dna, k, n)
        if iterScore < recordScore:
            recordScore = iterScore
            recordMotifs = iterMotifs
    return recordMotifs, recordScore


if __name__ == '__main__':
#    prof = constructProbabilityProfile(['GACC'])
#    for l in prof:
#        print l
    theMotifs, score = gibbsSampling(['CGCCCCTCTCGGGGGTGTTCAGTAAACGGCCA',
                                              'GGGCGAGGTATGTGTAAGTGCCAAGGTGCCAG',
                                              'TAGTACCGAGACCGAAAGAAGTATACAGGCGT',
                                              'TAGATCAAGTTTCAGGTGCACGTCGGTGAACC',
                                              'AATCCACCAGCTCCACGTGCAATGTTGGCCTA'],
                                              8, 20, 1000)
    print theMotifs, score
