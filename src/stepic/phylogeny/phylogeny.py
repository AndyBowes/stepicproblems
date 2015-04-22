import networkx as nx
import operator
import re
from itertools import ifilterfalse, chain
from copy import deepcopy

def buildGraph(edges):
    """
    Build a Graph from a list of edge triplet tuples
    """
    graph = nx.Graph()
    for i, j, d in edges:
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
    leafNodes = [node for node, degree in graph.degree_iter() if degree == 1]
    for i in leafNodes:
        print '\t'.join([str(nx.shortest_path_length(graph, i, j, weight='weight')) for j in leafNodes])


def calculateLimbLength(node, distanceMatrix):
    """
    Find the Limb Length of the given Node ID
    """
    def _innerCalc():
        l = len(distanceMatrix)
        for i in ifilterfalse(lambda x: x == node, range(l - 1)) :
            for k in ifilterfalse(lambda x: x == node, range(i + 1, l)):
                # print "Inner Calc: {0} : {1}".format(i,k)
                try:
                    yield ((distanceMatrix[i][node]
                            + distanceMatrix[k][node]
                            - distanceMatrix[i][k]) / 2)
                except IndexError as e:
                    print "Index Error: {0} {1} {2}".format(i, k, node)
                    raise e
    return min(_innerCalc())

def findJoinPoint(node, distanceMatrix):
    l = len(distanceMatrix)
    for i in ifilterfalse(lambda x: x == node, range(l - 1)) :
        for k in ifilterfalse(lambda x: x == node, range(i + 1, l)):
            if (distanceMatrix[node][i] + distanceMatrix[node][k]) == distanceMatrix[i][k]:
                return i, k

def getLimbLength(limbLengthFile):
    node = int(limbLengthFile.readline())
    distanceMatrix = [map(int, line.strip().split(' ')) for line in limbLengthFile]
    return calculateLimbLength(node, distanceMatrix)

def removeEntry(distanceMatrix, index):
    """
    """
    newMatrix = [list(chain(x[:index], x[index + 1:])) for x in distanceMatrix]
    del newMatrix[index]
    return newMatrix

def additivePhylogenyFromFile(distanceMatrixFile, separator='\t'):
    """
    Reconstruct a graph from a distance matrix file
    Output the edges from the tree
    """
    distanceMatrix = [map(int, line.strip().split(separator)) for line in distanceMatrixFile]
    nodeIds = range(len(distanceMatrix))
    nextNode = len(distanceMatrix)

    _, graph = additivePhylogeny(nextNode, nodeIds, distanceMatrix)

    # graph = reconstructGraph(distanceMatrix)
    for adjacency in graph.adjacency_iter():
        for k, v in adjacency[1].items():
            yield adjacency[0], k, v['weight']

def additivePhylogeny(nextNode, nodeIds, distanceMatrix):
    """
    Recursive function to build a graph from the distance matrix
    """
    if len(nodeIds) == 2:
        graph = nx.Graph()
        graph.add_edge(nodeIds[0], nodeIds[1], {'weight':distanceMatrix[0][1]})
        return nextNode, graph

    # print "Distance Matrix: {0}".format(distanceMatrix)
    limbLengths = [calculateLimbLength(i, distanceMatrix) for i in range(len(nodeIds))]
    minIndex, minLimbLength = min(enumerate(limbLengths), key=operator.itemgetter(1))

    leafNodeId = nodeIds[minIndex]

    baldMatrix = deepcopy(distanceMatrix)
    # Adjust the remaining lengths in the column, row
    baldMatrix[minIndex] = [x - minLimbLength for x in baldMatrix[minIndex]]
    for i in ifilterfalse(lambda x:x == minIndex, range(len(nodeIds))):
        baldMatrix[i][minIndex] -= minLimbLength

    nextNodes = deepcopy(nodeIds)
    del nextNodes[minIndex]
    nextNode, graph = additivePhylogeny(nextNode, nextNodes, removeEntry(distanceMatrix, minIndex))

    # Attach the leaf node at the appropriate point in the returned graph
    i, k = findJoinPoint(minIndex, baldMatrix)
    path = nx.shortest_path(graph, nodeIds[i], nodeIds[k], weight="weight")
    limbLength2 = baldMatrix[i][minIndex]
    i = 0
    while graph[path[i]][path[i + 1]]['weight'] < limbLength2:
        limbLength2 -= graph[path[i]][path[i + 1]]['weight']
        i += 1
    if limbLength2 == 0:
        graph.add_edge(path[i], leafNodeId, {'weight':minLimbLength})
    else:
        totalLength = graph[path[i]][path[i + 1]]['weight']
        graph.add_edge(path[i], nextNode, {'weight':limbLength2})
        graph.add_edge(path[i + 1], nextNode, {'weight':totalLength - limbLength2})
        graph.add_edge(nextNode, leafNodeId, {'weight':minLimbLength})
        graph.remove_edge(path[i], path[i + 1])
        nextNode += 1

    return nextNode, graph

if __name__ == '__main__':
#    with open("data/edges.txt") as fp:
#        generateDistanceMatrix(fp)
#        edges = [(0,4,11),(1,4,2),(2,5,6),(3,5,7),(4,5,4)]
#    with open("data/limbLength.txt") as fp:
#        print getLimbLength(fp)
    with open("data/additivePhylogeny.txt") as fp:
        for i, j, w in additivePhylogenyFromFile(fp, separator=' '):
            print "{0}->{1}:{2}".format(i, j, w)
