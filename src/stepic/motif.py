'''
Created on 16 Nov 2013

@author: Andy Bowes
'''
from itertools import permutations, product

def getKmers(dna,k):
    """
    Find all the K-mers in a DNA sequence
    """
    for i in range(len(dna)-k):
        yield dna[i:i+k]

def getKmerVariations(kmer,d):
    """
    Find all the possible variations on a kmer with at most d differences
    """
    def applyWildCard(char, pattern):
        if pattern == '1': return ['A','C','G','T'] 
        return [char]
    maskPattern = '1' * d + '0' * (len(kmer) - d)
    patterns = ["".join(p) for p in set(permutations(maskPattern))]
    variations = [ ''.join(k) for p in patterns for k in product(*map(applyWildCard,kmer,p))]
    return variations

def motifEnumeration(dna,k,d):
    kmers = set([kmer for seq in dna for kmer in getKmers(seq, k) ])
    variants = sorted(set([v for kmer in kmers for v in getKmerVariations(kmer, d)]))
    for v in variants:
        v2 = getKmerVariations(v, d)
        for seq in dna:
            if not any([x in seq for x in v2]):
                break 
        else:
            yield v

if __name__ == '__main__':
    kmers = motifEnumeration(['ATTTGGC','TGCCTTA','CGGTATC','GAAAATT'], 3, 1)
    print ' '.join(kmers)
    #getKmerVariations('CAT', 1)
    #patterns = ['100','010','001']
    #print [ ''.join(k) for p in patterns for k in product(*map(applyWildCard,'CAT',p))]
     