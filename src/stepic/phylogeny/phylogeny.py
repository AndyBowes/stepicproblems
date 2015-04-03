import networkx as nx
import operator
import re
from itertools import ifilterfalse

def buildGraph(edges):
    """
    Build a Graph from a list of edge triplet tuples
    """
    graph = nx.Graph()
    for i,j,d in edges:
        if i < j:
            graph.add_edge(i, j, {'weight':d})
    return graph

def readEdgesFile(edgesFile):
    """
    
    """
    pattern = re.compile(r"(\d*)->(\d*):(\d*)")
    for line in edgesFile:
        yield map(int, pattern.match(line).groups())
        
def generateDistanceMatrix(edgesFile):
    """
    Print the Distance Matrix as defined from the Edges in the input file
    """
    edges = readEdgesFile(fp)   
    graph = buildGraph(edges)
    leafNodes = [node for node,degree in graph.degree_iter() if degree==1]
    for i in leafNodes:
        print '\t'.join([str(nx.shortest_path_length(graph,i,j,weight='weight')) for j in leafNodes])


def calculateLimbLength(node, distanceMatrix):
    """
    Find the Limb Length of the given Node ID
    """
    def _innerCalc():
        l = len(distanceMatrix)
        for i in ifilterfalse(lambda x: x==node,range(l-1)) :
            for k in ifilterfalse(lambda x: x==node,range(i,l)):
                yield ((distanceMatrix[i][node]
                         + distanceMatrix[k][node]
                         - distanceMatrix[i][k])/2)
    return min(_innerCalc())

def getLimbLength(limbLengthFile):
    node = int(limbLengthFile.readline())
    distanceMatrix = [map(int, line.strip().split(' ')) for line in limbLengthFile]
    return calculateLimbLength(node, distanceMatrix)
    

def reconstructGraph(distanceMatrix):
    """
    """
    def getEdges():
        nodeIds = range(len(distanceMatrix))
        nextNode = len(distanceMatrix)
        while len(nodeIds) > 2:
            limbLengths = [calculateLimbLength(i, distanceMatrix) for i in range(nextNode)]
            minIndex, minLimbLength = min(enumerate(limbLengths), key=operator.itemgetter(1))
            
            # Yield 1st Edge to new node
            yield nodeIds[minIndex],nextNode, minLimbLength
            nodeIds[minIndex] = nextNode
            
            # Adjust the remaining lengths in the column, row
            distanceMatrix[minIndex] = [x - minLimbLength for x in distanceMatrix[minIndex]]
            for i in ifilterfalse(lambda x:x==minIndex, range(len(nodeIds))):
                distanceMatrix[i][minIndex] -= minLimbLength
            # Reset the diagonal element to zero
            distanceMatrix[minIndex][minIndex] = 0
            
            # Find the 2nd node (index of 1st match where limLength[i] = distanceMatch[minIndex][i]
            
            # Yield 2nd Edge to new node
            yield nodeIds[index2],nextNode,limbLength2
            
            # Remove the row & column for the 2nd Node
            
            del nodeIds[index2]
            
            nextNode += 1
            
        # Yield the final edge
        yield nodeIds[0], nodeIds[1], distanceMatrix[0][1] 

    return getEdges()

def additivePhylogeny(distanceMatrixFile):
    """
    Reconstruct a graph from a distance matrix file
    Output the edges from the tree
    """
    distanceMatrix = [map(int, line.strip().split('\t')) for line in distanceMatrixFile]
    
    graph = reconstructGraph(distanceMatrix)
    for adjacency in graph.adjacency_iter():
        for k,v in adjacency[1].items():
            yield adjacency[0],k, v['weight']


if __name__ == '__main__':
#    with open("data/edges.txt") as fp:
#        generateDistanceMatrix(fp)
#        edges = [(0,4,11),(1,4,2),(2,5,6),(3,5,7),(4,5,4)]
    with open("data/limbLength.txt") as fp:
        print getLimbLength(fp)
            

