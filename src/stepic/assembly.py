"""
Created on 25 Nov 2013

"""
from collections import defaultdict, deque
from itertools import product

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
    # Build Double Linked List
    tour = []
    unusedEdges = deque([])
    def doTour(key):
        while key in adjacencyList:
            yield key
            values = adjacencyList[key]
            key1 = values.pop()
            if len(values) > 0:
                adjacencyList[key] = values
                unusedEdges.append(key)
            else:
                adjacencyList.pop(key)
            key = key1
        yield key

    tour = [ x for x in doTour(adjacencyList.keys()[0])]
    while len(adjacencyList) > 0:
        key = unusedEdges.pop()
        if key in adjacencyList:  # It is possible that a key has been used by another tour
            newTour = [x for x in doTour(key)]
            # Splice into existing tour
            startPos = tour.index(key)
            tour = tour[:startPos] + newTour + tour[startPos + 1:]
    return tour


def eulerianPath(adjacencyList):
    """
    This is an Open Eulerian Path.
    Find the 2 ends, all nodes will have the same number of incoming & outgoing nodes except the Start & Finish Nodes
    Join the 2 ends from Finish to Start and it will produce a Eulerian Cycle which can be solved as above.
    """
    outCount = defaultdict(int)
    inCount = defaultdict(int)
    for k, v in adjacencyList.iteritems():
        outCount[k] = len(v)
        for n in v:
            inCount[n] += 1
    startNode = [k for k, v in outCount.iteritems() if v > inCount[k]][0]
    endNode = [k for k, v in inCount.iteritems() if v > outCount[k]][0]
    values = adjacencyList.get(endNode, [])
    values.extend([startNode])
    adjacencyList[endNode] = values
    tour = eulerianCycle(adjacencyList)
    # Break the Tour after the End Node to get the Path
    endPos = tour.index(endNode)
    result = deque(tour[:-1])
    result.rotate(-1 * (endPos + 1))
    return result

def stringReconstruction(adjacencyList):
    kmers = eulerianPath(adjacencyList)
    return kmers[0][:-1] + "".join([x[-1] for x in kmers])

def universalString(n):
    elements = [ "".join(p) for p in  product(['0', '1'], repeat=n)]
    adjacencyList = defaultdict(list)
    for e in elements:
        adjacencyList[e[:-1]].append(e[1:])
    return eulerianCycle(adjacencyList)

if __name__ == '__main__':  # pragma: no cover
#    print debruinGraph('AAGATTCTCTAC', 4)
#    print "->".join([str(x) for x in eulerianCycle({0:[3], 1:[0], 2:[1, 6], 3:[2], 4:[2], 5:[4], 6:[5, 8], 7:[9], 8:[7], 9:[6]})])
#    print "->".join([str(x) for x in eulerianPath({0:[2], 1:[3], 2:[1], 3:[0, 4], 6:[3, 7], 7:[8], 8:[9], 9:[6]})])
#    print stringReconstruction({'CTT':['TTA'], 'ACC':['CCA'], 'TAC':['ACC'], 'GGC':['GCT'], 'GCT':['CTT'], 'TTA':['TAC']})
    print universalString(16)
