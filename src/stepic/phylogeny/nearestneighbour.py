'''
Created on 19 Apr 2015

@author: Andy
'''
from phylogeny import removeEntry
import networkx as nx

def constructNearestNeighbourMatrix(distanceMatrix):
    """
    Build the nearest neighbour matrix for a supplied distance matrix
    """
    totalDistances = [sum(row) for row in distanceMatrix]
    n = len(distanceMatrix)
    neighbourMatrix = [ [(n-2)*d - totalDistances[i] - totalDistances[j] 
                                    for j, d in enumerate(distanceMatrix[i])]
                                    for i in range(len(distanceMatrix))]
    for i in range(n):
        neighbourMatrix[i][i] = 0
    return neighbourMatrix

def findMinimumElement(matrix):
    """
    """
    minValue=9999999
    minLocation = None
    for i in range(len(matrix)-1):
        for j in range(i, len(matrix)):
            if matrix[i][j] < minValue:
                minLocation = i,j
                minValue = matrix[i][j]
    return minLocation
    
    
def neighbourJoining(nodeIds, nextNode, distanceMatrix):
    """
    """
    if len(distanceMatrix) == 2:
        graph = nx.Graph()
        graph.add_edge(nodeIds[0],nodeIds[1],{'weight':distanceMatrix[0][1]})
        return graph
    
    neighbourMatrix = constructNearestNeighbourMatrix(distanceMatrix)
    i,j = findMinimumElement(neighbourMatrix)
    deltaLength = (sum(distanceMatrix[i])-sum(distanceMatrix[j]))/(len(distanceMatrix)-2)
    limbLength1 = (distanceMatrix[i][j] + deltaLength)/2.0
    limbLength2 = (distanceMatrix[i][j] - deltaLength)/2.0
    node1 = nodeIds[i]
    node2 = nodeIds[j]
    
    # Add new node to distance matrix
    for m in range(len(distanceMatrix)):
        distanceMatrix[m].append((distanceMatrix[m][i] + distanceMatrix[m][j] - distanceMatrix[i][j])/2.0)
    newRow = [ (distanceMatrix[m][i] + distanceMatrix[m][j] - distanceMatrix[i][j])/2.0 
                        for m in range(len(distanceMatrix))]
    newRow.append(0)
    distanceMatrix.append(newRow)
    nodeIds.append(nextNode)
    
    # Remove i & j elements
    distanceMatrix = removeEntry(removeEntry(distanceMatrix, j),i)
    nodeIds.pop(j)
    nodeIds.pop(i)
    
    graph = neighbourJoining(nodeIds,nextNode + 1, distanceMatrix)
    
    graph.add_edge(node1,nextNode,{'weight':limbLength1})
    graph.add_edge(node2,nextNode,{'weight':limbLength2})
    return graph

if __name__ == '__main__':
    with open("data/nearestNeighbour.txt") as fp:
        distanceMatrix = [map(int, line.strip().replace('\t',' ').split(' ')) for line in fp]
        tree = neighbourJoining(range(len(distanceMatrix)), len(distanceMatrix), distanceMatrix)
        for adjacency in tree.adjacency_iter():
            for k,v in adjacency[1].items():
                print '{0}->{1}:{2:.3f}'.format(adjacency[0],k, v['weight'])
