import networkx as nx
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
    
if __name__ == '__main__':
#    with open("data/edges.txt") as fp:
#        generateDistanceMatrix(fp)
#        edges = [(0,4,11),(1,4,2),(2,5,6),(3,5,7),(4,5,4)]
    with open("data/limbLength.txt") as fp:
        print getLimbLength(fp)
            

