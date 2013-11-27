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

def eulerianCycle(adjacencyList):
    """
    Walk through a Cyclical Eulerian Path
    """
    key = adjacencyList.keys()[0]
    while len(adjacencyList) > 0:
        yield key
        values = adjacencyList[key]
        key1 = values.pop()
        if len(values) > 0:
            adjacencyList[key] = values
        else:
            adjacencyList.pop(key)
        key = key1
    yield key



if __name__ == '__main__':  # pragma: no cover
#    print debruinGraph('AAGATTCTCTAC', 4)
     print "->".join([str(x) for x in eulerianCycle({0:[3], 1:[0], 2:[1, 6], 3:[2], 4:[2], 5:[4], 6:[5, 8], 7:[9], 8:[7], 9:[6]})])
