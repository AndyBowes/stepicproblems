'''
Created on 4 Mar 2015

@author: Andy
'''
from itertools import chain
from _functools import partial

class AbstractNode(object):
    
    def __init__(self, childNodes=None):
        self.childNodes = childNodes if childNodes else {}

    def isRoot(self):
        return False;

class SuffixTree(AbstractNode):
    
    def __init__(self, seq):
        super(SuffixTree, self).__init__(childNodes=None)
        self.seq = seq
        self.buildTree()
        
    def isRoot(self):
        return True;
    
    def buildTree(self):    
        for pos in range(len(self.seq)):
            node=self.childNodes.get(self.seq[pos],None)
            if node:
                node.addNode(self.seq,pos,pos)
            else:
                node= Node(pos,len(self.seq)-pos,pos)
                self.childNodes[self.seq[pos]] = node
        print(self)
    
    
    def apply(self, fn):
        """
        
        """
        yield chain([child.apply(fn) for child in self.childNodes.values()])
            
class Node(object):
    def __init__(self, ptr, length, leafPos=None, childNodes =None):
        self.startPos = ptr
        self.length = length
        self.childNodes = childNodes if childNodes else {}
        self.leafPos = leafPos

    def _isLeaf(self):
        return self.leafPos != None
    
    def addNode(self, seq, ptr, leafPos):
        """
        """
        # If the whole of this node matches then find the appropriate child node
        if seq[self.startPos:self.startPos + self.length] == seq[ptr:ptr + self.length]:
            ptr += self.length
            node=self.childNodes.get(seq[ptr],None)
            if node:
                node.addNode(seq,ptr,leafPos)
            else:
                self.childNodes[seq[ptr]] = Node(ptr,len(seq)-ptr,leafPos=leafPos)
        else:
            for i in range(self.length):
                if seq[self.startPos + i] != seq[ptr+i]:
                    break
            splitPos = i
            childNode1 = Node(self.startPos+splitPos, self.length-splitPos, 
                              leafPos=self.leafPos, childNodes=self.childNodes)
            childNode2 = Node(ptr+splitPos,len(seq)-(ptr+splitPos),leafPos=leafPos)
            self.length = splitPos
            self.childNodes = { seq[self.startPos+splitPos]: childNode1,
                                seq[ptr+splitPos]: childNode2}
            self.leafPos = None
            
    def apply(self, fn):
        chain([fn(self)],[child.apply(fn) for child in self.childNodes.values()])

def printNode(node, seq=None):
    print("Visiting node:{0} : {1}".format(node.startPos, seq[node.startPos:node.startPos+node.length]))
    return seq[node.startPos:node.startPos+node.length]

if __name__ == '__main__':
    seq = 'ACCTTAGTC$'
    tree = SuffixTree(seq)
    fn = partial(printNode, seq=seq)
#    results = tree.apply( lambda node : tree.seq[node.startPos:node.startPos+node.length])
    for r in tree.apply(fn):
        print r