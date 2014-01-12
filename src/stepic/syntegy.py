"""
Created on 5 Jan 2014

"""
from dna import reverseComplement
from motif import getKmers
from collections import defaultdict

def _printSequence(sequence):
    print '(' + ' '.join("%+d" % (x) for x in sequence) + ')'

def greedySorting(sequence):
    reversalDistance = 0
    for k in range(0, len(sequence)):
        if abs(sequence[k]) != k + 1:
           # Rotate sequence between k + location of value
           pos = sequence.index(k + 1) if k + 1 in sequence else sequence.index((k + 1) * -1)
           block = list(reversed([-x for x in sequence[k:pos + 1]]))
           for i in range(len(block)):
               sequence[k + i] = block[i]
           reversalDistance += 1
           _printSequence(sequence)
        if sequence[k] != k + 1:
           sequence[k] = abs(sequence[k])
           reversalDistance += 1
           _printSequence(sequence)
    return reversalDistance

def countBreakpoints(sequence):
    breakpoints = 0
    p = len(sequence)
    sequence = [0] + sequence + [p + 1]
    for x in range(1, len(sequence)):
        if (sequence[x - 1] >= 0 and sequence[x] != sequence[x - 1] + 1) or \
            (sequence[x - 1] < 0 and sequence[x] != sequence[x - 1] + 1):
            breakpoints += 1
    return breakpoints

def twoBreakDistance(genome1, genome2):
    """
    Calculate the 2 Break Distance between 2 genomes
    Each Genome is a List of Lists, each child List represents a chromosome
    """
    genome1Edges = {}
    genome2Edges = {}
    for chromosome in genome1:
        for i in range(len(chromosome) - 1):
            genome1Edges[chromosome[i]] = -1 * chromosome[i + 1]
            genome1Edges[chromosome[i + 1] * -1] = chromosome[i]
        genome1Edges[chromosome[-1]] = -1 * chromosome[0]
        genome1Edges[-1 * chromosome[0]] = chromosome[-1]
    for chromosome in genome2:
        for i in range(len(chromosome) - 1):
            genome2Edges[chromosome[i]] = -1 * chromosome[i + 1]
            genome2Edges[chromosome[i + 1] * -1] = chromosome[i]
        genome2Edges[chromosome[-1]] = -1 * chromosome[0]
        genome2Edges[-1 * chromosome[0]] = chromosome[-1]

    noOfCycles = 0
    while len(genome1Edges) > 0:
        noOfCycles += 1
        # Take the 1st Edge from Genome 1 & keep going until we return to this point.
        start = genome1Edges.keys()[0]
        source = start
        direction = True
        while True:
            edges = genome1Edges if direction else genome2Edges
            source = edges.pop(source)
            edges.pop(source)
            direction = not direction
            if source == start:
                break
    noOfBlocks = sum([len(g) for g in genome1])
    return noOfBlocks - noOfCycles


def syntegenyBlockConstruction(kLength, sequence1, sequence2):
    kmerPos = defaultdict(list)
    for i in range(len(sequence1) - kLength + 1):
        kmer = sequence1[i:i + kLength]
        kmerPos[kmer].append(i)
        kmerPos[reverseComplement(kmer)].append(i)

    for i in range(len(sequence2) - kLength + 1):
        kmer = sequence2[i:i + kLength]
        for pos in kmerPos[kmer]:
            yield(pos, i)

if __name__ == '__main__':  # pragma: no cover
#    greedySorting([-3, +4, +1, +5, -2])
#    print countBreakpoints([+3, +4, +5, -12, -8, -7, -6, +1, +2, +10, +9, -11, +13, +14])
#    genome1 = [[+1, +2, +3, +4, +5, +6]]
#    genome2 = [[+1, -3, -6, -5][+2, -4]]
#    print twoBreakDistance(genome1, genome2)
#    kmerPos = syntegenyBlockConstruction(3, 'AAACTCATC', 'TTTCAAATC')
#    for pos in kmerPos:
#        print pos
    print twoBreakDistance([[1, 2, 3, 4, 5, 6]], [[+1, -3, -6, -5], [+2, -4]])

