'''
Created on 27 May 2013

@author: Andy
'''

class Edge(object):
    def __init__(self, value, children=None, starts=None):
        self.value = value
        if children == None:
            children = []
        if starts == None:
            starts = []
        self.children = children
        self.starts = starts
    
    def addEdge(self, sequence, startPos):
        edges = [e for e in self.children if e.value.startswith(sequence[0])]
        if sequence == self.value:
            self.starts.append(startPos)  
        elif len(edges) > 0:
            child = edges[0]
            if sequence.startswith(child.value):
                child.addEdge(sequence[len(child.value):], startPos)
            else:
                child.splitEdge(sequence, startPos)
        else:
            self.children.append(Edge(sequence, None, startPos))
    
    def splitEdge(self, sequence, startPos):
        i = 0
        try:
            while  i < len(self.value) and i < len(sequence) and sequence[i] == self.value[i]: i += 1
            
            edge1 = Edge(self.value[i:], self.children, self.starts)
            edge2 = Edge(sequence[i:], None, [startPos])
            self.value = self.value[:i]
            self.children = [edge1, edge2]
        except IndexError:
            print 'Number of out range {0} : {1} : {2}'.format(i, len(self.value), len(sequence))

    def doWalk(self):
        print self.value
        for e in self.children : e.doWalk()
        
    def getStartPositions(self, sequence, mismatches=0):
        if len(self.children) == 0:
            yield self.starts
        else:
            if sequence.startswith(self.value):
                pass

def suff(sequence):
    rootEdge = Edge('', None, None)
    print("Start")
    for i in range(len(sequence)):
        print "Ere I am J.H"
        rootEdge.addEdge(sequence[i:],i)
    
    return rootEdge.doWalk()


if __name__ == '__main__':
    suff('ATTTGGATT$')