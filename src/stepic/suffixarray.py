"""
Created on 13 Jan 2014

"""
from collections import deque

def buildSuffixArray(sequence):
    """
    Create a Suffix Array for a Sequence
    """
    array = [i for i in range(len(sequence))]
    array.sort(lambda x, y: cmp(sequence[x:x + 10000], sequence[y:y + 10000]))
    return array

def getSuffixEdges(sequence, suffixArray, lcpvalues):
    """
    Convert a Suffix Array into a List of Suffix Tree edges
    """
    prevEdges = deque([lcpvalues[0]])
    for i in range(1, len(lcpvalues)):
        lcp = lcpvalues[i]
        # print prevEdges, lcp
        if lcp > prevEdges[-1]:
            prevEdges.append(lcp)
        endPos = len(sequence) + 1
        while prevEdges and prevEdges[-1] >= lcp:
            startPos = prevEdges.pop()
            yield sequence[suffixArray[i - 1]:][startPos:endPos]
            endPos = startPos
        prevEdges.append(lcp)
    endPos = len(sequence) + 1
    while prevEdges:
        startPos = prevEdges.pop()
        yield sequence[suffixArray[-1]:][startPos:endPos]
        endPos = startPos



if __name__ == '__main__':  # pragma: no cover
#    print ', '.join([str(x) for x in buildSuffixArray('AACGATAGCGGTAGA$')])
    for e in getSuffixEdges('GTAGT$', [5, 2, 3, 0, 4, 1], [0, 0, 0, 2, 0, 1]):
        print e
