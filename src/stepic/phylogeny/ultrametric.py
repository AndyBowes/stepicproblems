'''
Created on 14 Apr 2015

@author: Andy
'''
import networkx as nx
from phylogeny import removeEntry

def findLowestElement(distanceMatrix):
    """
    Find the position of the lowest entry in a symmetric distance matrix
    """
    minValue = 99999999
    minPos = None
    for i in range(len(distanceMatrix)-1):
        for j in range(i+1,len(distanceMatrix)):
            if distanceMatrix[i][j] < minValue:
                minValue = distanceMatrix[i][j]
                minPos = i,j
    return minPos

def ultrametricTree(distanceMatrix):
    graph = nx.Graph()
    for nodeId in range(len(distanceMatrix)):
        graph.add_node(nodeId, {'age':0,
                                'size':1.0})
    nodeIds = range(len(distanceMatrix))
    nextNode = len(distanceMatrix)
    #print('Added nodes')
    while len(distanceMatrix)> 1:
        i,j = findLowestElement(distanceMatrix)
        nodeAge = distanceMatrix[i][j]/2.0
        sizei = graph.node[nodeIds[i]]['size']
        sizej = graph.node[nodeIds[j]]['size']
        graph.add_node(nextNode, {'age': nodeAge, 'size': sizei + sizej})
        graph.add_edge(nodeIds[i], nextNode, {'weight': nodeAge - graph.node[nodeIds[i]]['age']})
        graph.add_edge(nodeIds[j], nextNode, {'weight': nodeAge - graph.node[nodeIds[j]]['age']})
        
        for ptr in range(len(distanceMatrix)):
            distanceMatrix[ptr].append( ((distanceMatrix[ptr][i]*sizei) + (distanceMatrix[ptr][j]*sizej))/(sizei+sizej))
        newElement = [((distanceMatrix[i][ptr]*sizei) + (distanceMatrix[j][ptr]*sizej))/(sizei+sizej) for ptr in range(len(distanceMatrix))]
        newElement.append(0)
        distanceMatrix.append(newElement)
        
        nodeIds.append(nextNode)
        nextNode += 1
        
        distanceMatrix = removeEntry(removeEntry(distanceMatrix, j),i)
        nodeIds.pop(j)
        nodeIds.pop(i)
        #print('Processed item')
        #print(distanceMatrix)
    return graph

if __name__ == '__main__':
    with open('data/ultrametric_1.txt') as distanceMatrixFile:
        distanceMatrix = [map(int, line.strip().split('\t')) for line in distanceMatrixFile]
        #print('Start')
        tree=ultrametricTree(distanceMatrix)
        #tree = ultrametricTree(distanceMatrix)
        for adjacency in tree.adjacency_iter():
            for k,v in adjacency[1].items():
                print '{0}->{1}:{2:.3f}'.format(adjacency[0],k, v['weight'])
        
        