"""
Created on 10 Jan 2014

"""
import re

class IdGenerator(object):
    def __init__(self):
        self.id = 0

    def nextId(self):
        self.id += 1
        return self.id

class Edge(object):
    def __init__(self, value, parentId, idGenerator):
        self.value = value
        self.children = {}
        self.parentId = parentId
        self.idGenerator = idGenerator
        self.id = idGenerator.nextId()
        self.positions = []

    def addSequence(self, sequence, pos=-1):
        edge = self.children.get(sequence[0], None)
        if not edge:
            edge = Edge(sequence[0], self.id, self.idGenerator)
            self.children[sequence[0]] = edge
        edge.addPosition(pos)
        return edge

    def addPosition(self, pos):
        if pos >= 0:
            self.positions.append(pos)

    def walkTree(self):
        """
        Walk through the Trie printing the details of each node 
        """
        if self.parentId:
            print self.parentId, self.id, self.value
        for child in self.children.itervalues():
            child.walkTree()

    def findPositions(self, seq):
        """
        Find locations of sequence in the Trie
        """
        child = self.children.get(seq[0], None)
        if child:
            if len(seq) == 1:
                return child.positions
            return child.findPositions(seq[1:])
        else:
            return []

def buildTrie(sequences):
    idGenerator = IdGenerator()
    root = Edge('', None, idGenerator)
    i = 0
    for seq in sequences:
        edge = root
        while len(seq) > 0:
            edge = edge.addSequence(seq, i)
            seq = seq[1:]
        i += 1
        print i
    return root

def generateSequences(sequence):
    seq = sequence + '$'
    for i in range(len(seq)):
        yield seq[i:]

def findMatches(sequence, patterns):
    """
    Find the location of all of the Patterns in the Sequence
    """
#
#
#     idGenerator = IdGenerator()
#     root = Edge('', None, idGenerator)
#     i = 0
#     sequence = sequence + '$'
#     print len(sequence)
#     for i in range(len(sequence)):
#         seq = sequence[i:]
#         edge = root
#         while len(seq) > 0:
#             edge = edge.addSequence(seq, i)
#             seq = seq[1:]
#         print i
    # root = buildTrie(generateSequences(sequence))
    matches = [[m.start() for m in re.finditer('(?=' + pattern + ')', sequence)] for pattern in patterns]
    return matches


if __name__ == '__main__':  # pragma: no cover
#    trie = buildTrie(['GGTA', 'CG', 'GGC'])
#    trie.walkTree()
    matches = findMatches('AATCGGGTTCAATCGGGGT', ['ATCG', 'GGGT'])
    for match in matches:
        if len(match) > 0:
            print ' '.join([str(x) for x in match])
