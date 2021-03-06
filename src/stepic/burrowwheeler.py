"""
Created on 14 Jan 2014

"""
from stepic.suffixarray import buildSuffixArray
from stepic.motif import getKmers
from itertools import chain, takewhile
from collections import Counter, defaultdict

def burrowWheelerTransform(sequence):
    """
    Perform Burrow Wheeler Transform
    """
    array = [i for i in range(len(sequence))]
    array.sort(lambda x, y: cmp(buffer(sequence, x, 10000), buffer(sequence, y, 10000)))
    return ''.join([sequence[x - 1] for x in array])

def inverseBurrowWheelerTransform(sequence):
    """
    Reverse the Burrow Wheeler Transform
    """
    mapping = sorted([(i, v) for i, v in enumerate(sequence)], key=lambda x: x[1])
    first = [m[1] for m in mapping]
    firstLast = [m[0] for m in mapping]
    def process():
        pos = 0
        while firstLast[pos] != 0:
            pos = firstLast[pos]
            yield first[pos]
        yield '$'
    return ''.join(process())

def firstLast(bwt):
    mapping = sorted([(i, v) for i, v in enumerate(bwt)], key=lambda x: x[1])
    first = ''.join([m[1] for m in mapping])
    firstToLast = [m[0] for m in mapping]
    lastToFirst = [x[0] for x in sorted([(i, v) for i, v in enumerate(firstToLast)], key=lambda y: y[1])]
    return first, lastToFirst

def findPatterns(bwt, patterns):
    """
    Find number of matches of multiple Patterns in the sequence
    """
    first, lastToFirst = firstLast(bwt)
    for pattern in patterns:
        yield bwmatching(pattern, bwt, lastToFirst)

def bwmatching(pattern, lastColumn, lastToFirst):
    top = 0
    bottom = len(lastColumn)
    while top <= bottom:
        if pattern:
            symbol = pattern[-1]
            pattern = pattern[:-1]
            if symbol in lastColumn[top:bottom + 1]:
                topIndex = lastColumn.index(symbol, top, bottom + 1)
                bottomIndex = lastColumn.rindex(symbol, top, bottom + 1)
                top = lastToFirst[topIndex]
                bottom = lastToFirst[bottomIndex]
            else:
                return []
        else:
            break
    return range(top, bottom + 1)

def multiPatternMatching(sequence, patterns):
    bwt = burrowWheelerTransform(sequence)
    suffixArray = buildSuffixArray(sequence)

    for match in findPatterns(bwt, patterns):
        for pos in match:
            yield suffixArray[pos]

def patternMatchWithMismatches(sequence, patterns, maxMismatches):
    """
    Find locations of Patterns in the Sequence which have <= No of Mismatches
    """
    bwt = burrowWheelerTransform(sequence)
    suffixArray = buildSuffixArray(sequence)
    _, lastToFirst = firstLast(bwt)
    for pattern in patterns:
        fragmentIndexes = list(findSeedPositions2(bwt, lastToFirst, pattern, maxMismatches))
        candidatePos = Counter([suffixArray[y] - offset for offset, x in fragmentIndexes for y in x])
        seedPositions = [cp[0] for cp in takewhile(lambda x : x[1] > 1, candidatePos.most_common())]
        for pos in seedPositions:
            if isSimilar(sequence[pos:pos + len(pattern)], pattern, maxMismatches):
                yield pos
#            if pos in [14, 16, 57, 63, 69]:
#                print "Missed : {0} : {1} : {2}".format(pos, pattern, sequence[pos:pos + len(pattern)])
#            print "Found : {0} : {1}".format(pattern, pos)
#            if isSimilar(sequence[pos:pos + len(pattern)], pattern, maxMismatches):
#                print "Match : {0} : {2} : {1}".format(pattern, sequence[pos:pos + len(pattern)], pos)

def findSeedPositions2(bwt, lastToFirst, pattern, maxMismatches):
    fragments = list(splitPattern(pattern, maxMismatches + 4))
    for fragment in fragments:
        yield fragment[0], bwmatching(fragment[1], bwt, lastToFirst)


def findSeedPositions(bwt, lastToFirst, pattern, maxMismatches):
    fragments = list(splitPattern(pattern, maxMismatches + 1))
    def expandLeft(pos, ptr):
        mismatches = 0
        while mismatches <= maxMismatches:
            if pos == 0:
                break
            pos -= 1
            ptr = lastToFirst[ptr]
            if ptr == 0:
                mismatches = maxMismatches + 1
            else:
                if pattern[pos] != bwt[ptr]:
                    mismatches += 1
        return maxMismatches

    def expandRight():
        pass

    for fragment in fragments:
        # Get the Exact Matches on fragments and then extend to the Left & Right
        for ind in bwmatching(fragment[1], bwt, lastToFirst):
            if expandLeft(fragment[0], ind) <= maxMismatches:
                yield ind

def splitPattern(pattern, n):
    blockSize = (len(pattern) / n)
    startPos = 0
    while pattern:
        yield startPos, pattern[:blockSize]
        pattern = pattern[blockSize:]
        startPos += blockSize

def isSimilar(seq1, seq2, maxmismatches):
    if (len(seq1) != len(seq2)):
        return False
    mismatches = 0
    for i in range(len(seq1)):
        if seq1[i] != seq2[i]:
            mismatches += 1
            if mismatches > maxmismatches:
                break
    else:
        return True
    return False

def partialSuffixArray(sequence, freq):
    return [ (i, v) for i, v in enumerate(buildSuffixArray(sequence)) if v % freq == 0 ]


def findPatternWithMismatches(sequence, patterns, mismatches):
    KMER_LENGTH = 8
    seqKmers = defaultdict(list)
    for i in range(len(sequence) - KMER_LENGTH + 1):
        seqKmers[sequence[i:i + KMER_LENGTH]].append(i)

    for pattern in patterns:
        posCount = Counter()
        for i in range(len(pattern) - KMER_LENGTH + 1):
            posCount += Counter([pos - i for pos in seqKmers[pattern[i:i + KMER_LENGTH]]])
        for pos in [cp[0] for cp in takewhile(lambda x : x[1] > 6, posCount.most_common())]:
            if isSimilar(sequence[pos:pos + len(pattern)], pattern, mismatches):
                yield pos



if __name__ == '__main__':  # pragma: no cover
#    for o in findPatterns('TCCTCTATGAGATCCTATTCTATGAAACCTTCA$GACCAAAATTCTCCGGC', ['CCT', 'CAC', 'GAG', 'CAG', 'ATC']):
#        print o
    # print partialSuffixArray('PANAMABANANAS$', 5)
#    for pos in multiPatternMatching('AATCGGGTTCAATCGGGGT$', ['ATCG', 'GGGT']):
#        print pos
#    print ', '.join([ "{0}:{1}".format(sp, block) for sp, block in splitPattern('ABCD' * 7, 3)])
     print ' '.join([str(x) for x in patternMatchWithMismatches('ACATGCTACTTT$', ['ATT', 'GCC', 'GCTA', 'TATT'], 1)])
