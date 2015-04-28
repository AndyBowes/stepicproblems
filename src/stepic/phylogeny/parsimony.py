'''
Created on 19 Apr 2015

@author: Andy
'''

import networkx as nx
from itertools import repeat
from random import sample
import time

ALPHABET = 'ACGT'
MAX_INFINITY = 999999999

def findRoot(graph):
    """
    Find the Root Node in a directed Graph
    """
    nodeId = graph.nodes()[0]
    while len(graph.predecessors(nodeId)) > 0:
        nodeId = graph.predecessors(nodeId)[0]
    return nodeId


def smallParsimony(graph, calculateDNA=True):
    """
    Small Parsimony problem
    
    Given a rooted tree and the details the leaves, calculate the
    values of the internal nodes which give the smallest parsimony score.
    """
    rootNode = findRoot(graph)

    calculateParsimonyMatrix(graph, rootNode)

    # Once the Parsimony Matrix has been calculated then recreate the DNA for each node
    if calculateDNA:
        calculateNodeDna(graph, nodeId=rootNode)
    
    return graph.node[rootNode]['parsimonyScore'], graph

def calculateNodeDna(graph, parentDna=None, nodeId=None):
    """
    """
    if isLeaf(graph, nodeId):
        return
    matrix = graph.node[nodeId]['parsimony']
    if not parentDna:
        parentDna = repeat('X', len(matrix))
    
    dna = ''.join(map(selectCharacter, parentDna, matrix))
    #print 'DNA:{0}'.format(dna)
    graph.node[nodeId]['dna'] = dna

    for successorId in graph.successors(nodeId):
        calculateNodeDna(graph, parentDna=dna, nodeId=successorId)
    
def selectCharacter(parentChar, matrix):
    """
    Select the most appropriate character based on the parsimony matrix.
    
    If the parent character is in the list with minimum score then use that
    otherwise select random character from the chars with minimum score.
    """
    minValue = min(matrix.itervalues())
    minCharacters = [ k for k,v in matrix.iteritems() if v == minValue]
    return parentChar if parentChar in minCharacters else sample(minCharacters,1)[0]

def calculateCombinedParsimony(childParsimony1, childParsimony2):
    """
    
    """
    def calculateElement(matrix1, matrix2):
        return {char : min(v if k == char else v + 1 for k, v in matrix1.iteritems())
                        + min(v if k == char else v + 1 for k, v in matrix2.iteritems()) for char in ALPHABET}
    return map(calculateElement, childParsimony1, childParsimony2)

def calculateParsimonyMatrix(graph, nodeId):
    """
    Calculate the Parsimony Matrix at a node.
    
    If this is a rootNode then it can be calculated directly from the DNA,
    otherwise the details of the child matrixes will need to be combined.
    """
    if isLeaf(graph, nodeId):
        try:
            dna = graph.node[nodeId]['dna']
            parsimony = [{ x : 0 if x == char else MAX_INFINITY  for x in ALPHABET } for char in dna]
        except KeyError as e:
            print nodeId
            raise e
    else:
        childNodes = graph.successors(nodeId)
        childParsimony1 = calculateParsimonyMatrix(graph, childNodes[0])
        childParsimony2 = calculateParsimonyMatrix(graph, childNodes[1])
        parsimony = calculateCombinedParsimony(childParsimony1, childParsimony2)

    graph.node[nodeId]['parsimony'] = parsimony
    graph.node[nodeId]['parsimonyScore'] = sum((map(min, [x.itervalues() for x in parsimony])))
    return parsimony

def isLeaf(graph, nodeId):
    """
    Check if the given nodeId identifies a root node (i.e. it has no successors)
    """
    return len(graph.neighbors(nodeId)) <= 1

def readParsimonyFile(parsimonyFile):
    """
    Extract the details from the ParsimonyFile 
    returns a Graph with the initial nodes
    """
    graph = nx.DiGraph()
    numberOfLeaves = int(parsimonyFile.readline().strip())
    for nodeId in range(numberOfLeaves):
        parentId, dna = parsimonyFile.readline().strip().split('->')
        graph.add_node(nodeId, {'dna':dna, 'leaf':True})
        graph.add_edge(int(parentId), nodeId)

    for line in parsimonyFile.readlines():
        parentId, childId = map(int, line.strip().split('->'))
        graph.add_edge(parentId, childId)

    return graph

def readUnrootedTreeFile(lines):
    """
    Read the file containing the details of the Unrooted tree.
    
    Convert this to a rooted tree graph.
    Will need to add a root node & remove half of the edges
    """
    graph = nx.DiGraph()
    for line in lines:
        nodes = line.strip().split('->')
        graph.add_edge(nodes[0],nodes[1])
        for nodeId in nodes:
            if len(nodeId) > 1:
                graph.node[nodeId]['dna'] = nodeId

    return graph

def unrootedParsimony(graph, calculateDNA=True):
    """
    Perform parsimony on the supplied unrooted tree
    """
    addRootNode(graph)
    parsimonyScore, graph = smallParsimony(graph, calculateDNA=calculateDNA)
    graph = removeRootNode(graph)
    return parsimonyScore, graph

def addRootNode(graph):
    """
    Add a root node to an unrooted tree
    """
    # Add root node             
    edgeToBreak = graph.edges()[0]
    graph.add_edge('root',edgeToBreak[0])
    graph.add_edge('root',edgeToBreak[1])
    graph.remove_edge(edgeToBreak[0], edgeToBreak[1])
    if graph.has_edge(edgeToBreak[1], edgeToBreak[0]):
        graph.remove_edge(edgeToBreak[1], edgeToBreak[0])
        
    for nodeId, depth in nx.shortest_path_length(graph, 'root').iteritems():
        graph.node[nodeId]['depth'] = depth
    
    # Remove all edges pointing back up the tree
    for node1,node2 in graph.edges():
        if graph.node[node1]['depth'] > graph.node[node2]['depth']:
            graph.remove_edge(node1,node2)

def removeRootNode(graph, rootNode='root'):
    """
    Remove the root node & convert to a bidirectional tree
    """
    rootChildren = graph.successors(rootNode)
    graph.add_edge(rootChildren[0], rootChildren[1])
    graph.add_edge(rootChildren[1], rootChildren[0])
    graph.remove_node(rootNode)
    
    for edge in graph.edges():
        graph.add_edge(edge[1],edge[0])
    return graph

def getInternalEdges(graph):
    """
    Return all of the internal edges of a graph
    """
    return [e for e in graph.edges() if not ( isLeaf(graph, e[0]) or isLeaf(graph, e[1]))]


def getNeighbourGraphs(graph, node1, node2):
    """
    Generate the nearest neighbours of an unrooted tree/graph
    
    This returns 2 graphs
    """
    graph1 = graph.copy()
    graph2 = graph.copy()
    
    node1Neighbours = [x for x in graph.neighbors(node1) if x != node2]
    node2Neighbours = [x for x in graph.neighbors(node2) if x != node1]
    
    if len(node1Neighbours) < 2 or len(node2Neighbours) < 2:
        print node1Neighbours
        print node2Neighbours
    
    graph1.remove_edge(node1,node1Neighbours[0])
    if graph1.has_edge(node1Neighbours[0],node1):
        graph1.remove_edge(node1Neighbours[0],node1)
    graph1.remove_edge(node2,node2Neighbours[1])
    if graph1.has_edge(node2Neighbours[1],node2):
        graph1.remove_edge(node2Neighbours[1],node2)
    graph1.add_edge(node1,node2Neighbours[1])
    graph1.add_edge(node2Neighbours[1],node1)
    graph1.add_edge(node2,node1Neighbours[0])
    graph1.add_edge(node1Neighbours[0],node2)
    
    graph2.remove_edge(node1,node1Neighbours[0])
    if graph2.has_edge(node1Neighbours[0],node1):
        graph2.remove_edge(node1Neighbours[0],node1)
    graph2.remove_edge(node2,node2Neighbours[0])
    if graph2.has_edge(node2Neighbours[0],node2):
        graph2.remove_edge(node2Neighbours[0],node2)
    graph2.add_edge(node1,node2Neighbours[0])
    graph2.add_edge(node2Neighbours[0],node1)
    graph2.add_edge(node2,node1Neighbours[0])
    graph2.add_edge(node1Neighbours[0],node2)
    
    return [graph1, graph2]

def hammingDistance(sequence1,sequence2):
    return sum(map(lambda x, y: 1 if x != y else 0, sequence1, sequence2))


def printAdjacencyList(graph):
    for adjacency in graph.adjacency_iter():
        for k, v in adjacency[1].items():
            print '{0}->{1}'.format(adjacency[0], k)
    print('')    

def printDnaAdjacencyList(graph):
    for adjacency in graph.adjacency_iter():
        for k, v in adjacency[1].items():
            dna1 = graph.node[adjacency[0]]['dna']
            dna2 = graph.node[k]['dna']
            print '{0}->{1}:{2}'.format(dna1, dna2, hammingDistance(dna1,dna2)) 

def performLargeParsimony(graph):
    """
    Perform Large Parsimony on an unrooted tree
    """
    parsimonyScore, bestGraph=unrootedParsimony(graph, calculateDNA=True)
    
    while True:
        print parsimonyScore
        printDnaAdjacencyList(bestGraph)
        graphChanged = False
#         print getInternalEdges(bestGraph)
        for node1, node2 in getInternalEdges(bestGraph):
#             print bestGraph.edges()
            for neighbourGraph in getNeighbourGraphs(bestGraph, node1, node2):
                score, _ = unrootedParsimony(neighbourGraph, calculateDNA=True)
                if score < parsimonyScore:
                    parsimonyScore = score
                    bestGraph = neighbourGraph
                    graphChanged = True
        if not graphChanged:
            break
    
if __name__ == '__main__':
#     with open('data/smallParsimony_challenge.txt') as parsimonyFile:
#         start = time.time()
#         graph = readParsimonyFile(parsimonyFile)
#         parsimonyScore, graph = smallParsimony(graph)
#         print parsimonyScore
#         for adjacency in graph.adjacency_iter():
#             for k, v in adjacency[1].items():
#                 dna1 = graph.node[adjacency[0]]['dna']
#                 dna2 = graph.node[k]['dna']
#                 print '{0}->{1}:{2}'.format(dna1, dna2, hammingDistance(dna1,dna2))
#                 print '{1}->{0}:{2}'.format(dna1, dna2, hammingDistance(dna1,dna2))
#         end = time.time()

#     with open('data/unrootedParsimony_challenge.txt') as unrootedTreeFile:
#         start = time.time()
#         numberOfLeaves = unrootedTreeFile.readline()
#         graph = readUnrootedTreeFile(unrootedTreeFile.readlines())
#         parsimonyScore, graph = unrootedParsimony(graph)
#         print parsimonyScore
#         for adjacency in graph.adjacency_iter():
#             for k, v in adjacency[1].items():
#                 dna1 = graph.node[adjacency[0]]['dna']
#                 dna2 = graph.node[k]['dna']
#                 print '{0}->{1}:{2}'.format(dna1, dna2, hammingDistance(dna1,dna2))
#         end = time.time()

#     with open('data/parsimonyNearestNeighbour_challenge.txt') as unrootedTreeFile:
#         start = time.time()
#         node1,node2 = unrootedTreeFile.readline().strip().split(' ')
#         graph = readUnrootedTreeFile(unrootedTreeFile.readlines())
#  
#         for g in getNeighbourGraphs(graph, node1, node2):
#             for adjacency in g.adjacency_iter():
#                 for k, v in adjacency[1].items():
#                     print '{0}->{1}'.format(adjacency[0], k)
#             print('')
#         end = time.time()

    with open('data/largeParsimony_extra.txt') as unrootedTreeFile:
        start = time.time()
        unrootedTreeFile.readline()
        graph = readUnrootedTreeFile(unrootedTreeFile.readlines())
        performLargeParsimony(graph)
        end = time.time()
        print "Finished :{0}".format(end-start)
