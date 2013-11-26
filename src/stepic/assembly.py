"""
Created on 25 Nov 2013

"""
from collections import defaultdict

def stringComposition(seq, kmerLength):
    return sorted([seq[i:i + kmerLength] for i in range((len(seq) + 1) - kmerLength)])

def overlapGraph(kmers):
    adjacencyList = defaultdict(list)
    for kmer in kmers:
        adjacencyList[kmer[:-1]].append(kmer)
    return sorted(['{0} -> {1}'.format(kmer, s) for kmer in kmers for s in adjacencyList[kmer[1:]]])

def debruinGraph(seq, kmerLength):
    return debruinGraphFromKmers([seq[i:i + kmerLength] for i in range((len(seq) + 1) - kmerLength)])

def debruinGraphFromKmers(kmers):
    adjacencyList = defaultdict(list)
    for kmer in kmers:
        adjacencyList[kmer[:-1]].append(kmer[1:])
    return ['{0} -> {1}'.format(prefix, ','.join(sorted(adjacencyList[prefix]))) for prefix in sorted(adjacencyList.keys())]



if __name__ == '__main__':  # pragma: no cover
    print debruinGraph('AAGATTCTCTAC', 4)
