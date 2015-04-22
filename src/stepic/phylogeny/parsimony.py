'''
Created on 19 Apr 2015

@author: Andy
'''

import networkx as nx
import random

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


def smallParsimony(graph):
    """
    Small Parsimony problem
    
    Given a rooted tree and the details the leaves, calculate the
    values of the internal nodes which give the smallest parsimony score.
    """
    rootNode = findRoot(graph)

    calculateParsimonyMatrix(graph, rootNode)

    print "Parsimony Score:{0}".format(graph.node[rootNode]['parsimonyScore'])

    # Once the Parsimony Matrix has been calculated then recreate the DNA for each node

    return graph

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
    return len(graph.successors(nodeId)) == 0

def readParsimonyFile(parsimonyFile):
    """
    Extract the details from the ParsimonyFile 
    returns a Graph with the initial nodes
    """
    graph = nx.DiGraph()
    numberOfLeaves = int(parsimonyFile.readline().strip())
    for nodeId in range(numberOfLeaves):
        parentId, dna = parsimonyFile.readline().strip().split('->')
        graph.add_node(nodeId, {'dna':dna})
        graph.add_edge(int(parentId), nodeId)

    for line in parsimonyFile.readlines():
        parentId, childId = map(int, line.strip().split('->'))
        graph.add_edge(parentId, childId)

    return graph

if __name__ == '__main__':
    with open('data/smallParsimony_extra.txt') as parsimonyFile:
        graph = readParsimonyFile(parsimonyFile)

        for adjacency in graph.adjacency_iter():
            for k, v in adjacency[1].items():
                print '{0}->{1}'.format(adjacency[0], k)

        graph = smallParsimony(graph)

        print "Finished"
