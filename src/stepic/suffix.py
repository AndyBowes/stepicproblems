'''
Created on 27 May 2013

@author: Andy
'''

class Edge(object):
    def __init__(self, value, children=None):
        self.value = value
        if children == None:
            children = []
        self.children = children
    
    def addEdge(self, sequence):
        edges = [e for e in self.children if e.value.startswith(sequence[0])]
        if len(edges) > 0:
            child = edges[0]
            if sequence.startswith(child.value):
                child.addEdge(sequence[len(child.value):])
            else:
                child.splitEdge(sequence)
        else:
            self.children.append(Edge(sequence))
    
    def splitEdge(self, sequence):
        i = 0
        try:
            while  i < len(self.value) and i < len(sequence) and sequence[i] == self.value[i]: i += 1
            
            edge1 = Edge(self.value[i:], self.children)
            edge2 = Edge(sequence[i:])
            self.value = self.value[:i]
            self.children = [edge1, edge2]
        except IndexError:
            print 'Number of out range {0} : {1} : {2}'.format(i, len(self.value), len(sequence))

    def doWalk(self):
        print self.value
        for e in self.children : e.doWalk()

def suff(sequence):
    rootEdge = Edge('')
    print("Start")
    for i in range(len(sequence)):
        print "Ere I am J.H"
        rootEdge.addEdge(sequence[i:])
    
    return rootEdge.doWalk()


if __name__ == '__main__':
    with open('datafiles/rosalind_suff.txt') as fp:
        suff('ATTTGGATT$')