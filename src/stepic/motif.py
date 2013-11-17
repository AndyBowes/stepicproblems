'''
Created on 16 Nov 2013

@author: Andy Bowes
'''
from itertools import permutations, product

def getKmers(dna, k):
    """
    Find all the K-mers in a DNA sequence
    """
    for i in range(len(dna) - k):
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
    variations = [ ''.join(k) for p in patterns for k in product(*map(applyWildCard, kmer, p))]
    return variations

def motifEnumeration(dna, k, d):
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
    def checkChar(char1, char2):
        if char1 == char2: return 0
        return 1
    return sum([x for x in map(checkChar, seq1, seq2)])

def bestScore(dna, kmer):
    return min([ hammingDistance(kmer, sub) for sub in getKmers(dna, len(kmer))])

def medianString(dna, k):
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
    prob = 1.0
    for i in range(len(kmer)):
        prob *= profile[i]['ACGT'.index(kmer[i])]
    return prob

def probableKmer(dna, k, profile):
    kmers = getKmers(dna, k)
    bestKmer = ''
    bestProb = 0
    for kmer in kmers:
        prob = kmerProb(kmer, profile)
        if prob > bestProb:
            bestProb = prob
            bestKmer = kmer
    return bestKmer, bestProb

if __name__ == '__main__':
#    print hammingDistance('AAAAA', 'AATCA')
#    kmers = motifEnumeration(['ATTTGGC', 'TGCCTTA', 'CGGTATC', 'GAAAATT'], 3, 1)
#    print medianString(['AAATTGACGCAT', 'GACGACCACGTT', 'CGTCAGCGCCTG',
#                        'GCTGAGCACCGG', 'AGTACGGGACAG'], 3)
    print probableKmer('ACCTGTTTATTGCCTAAGTTCCGAACAAACCCAATATAGCCCGAGGGCCT', 5, [[0.2, 0.4, 0.3, 0.1],
                                                                                [0.2, 0.3, 0.3, 0.2],
                                                                                [0.3, 0.1, 0.5, 0.1],
                                                                                [0.2, 0.5, 0.2, 0.1],
                                                                                [0.3, 0.1, 0.4, 0.2]])
    # getKmerVariations('CAT', 1)
    # patterns = ['100','010','001']
    # print [ ''.join(k) for p in patterns for k in product(*map(applyWildCard,'CAT',p))]
