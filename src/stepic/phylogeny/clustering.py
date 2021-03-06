"""
Created on 28 Apr 2015

"""

from math import sqrt, exp
import operator
from itertools import imap
from collections import defaultdict
from _functools import partial
from ultrametric import findLowestElement
from phylogeny import removeEntry


def distance(point1, point2):
    """
    Calculate the distance between 2 n-dimensional points
    Points are supplied as a list with n floating point co-ordinates 
    """
    return sqrt(sum(map(lambda x, y:pow(x - y, 2), point1, point2)))

def readPoints(lines):
    """
    Extract the details of points from lines in a file
    """
    return [map(float, line.split(' ')) for line in lines]

def farthestFirstTraversal(centreCount, points):
    centres = [points[0]]
    while len(centres) < centreCount:
        centres.append(findFurthestPoint(centres, points))
    return centres

def findFurthestPoint(centres, points):
    """
    Find the point which is furthest from any of the centres
    """
    stats = {idx:min([distance(point, centre) for centre in centres]) for idx, point in enumerate(points)}
    idx, dist = max(stats.iteritems(), key=operator.itemgetter(1))
    return points[idx]

def squaredErrorDistortion(centres, points):
    """
    Calculate the squared error distortion
    """
    total = sum(map(lambda x : pow(x,2), [min([distance(point, centre) for centre in centres]) for point in points]))
    return total / len(points)

def findClosestCentre(point, centres):
    """
    Find the closest centre to the given point
    """
    stats = {idx:distance(point, centre) for idx, centre in enumerate(centres)}
    idx = min(stats.iteritems(), key=operator.itemgetter(1))[0]
    return idx
    
def averagePosition(points):
    """
    Find the average position of the given set of points
    """
    return [x/len(points) for x in map(sum, zip(*points))]

def lloydAlgorithm(centres, points):
    """
    Implement Lloyd Algorithm
    """
    prevCentres = []
    for i in range(1000):
        closestCentres = map(lambda point:findClosestCentre(point, centres),points)
        if closestCentres == prevCentres:
            print 'Located best solution: {0}'.format(i)
            break
        prevCentres = closestCentres
        centrePoints = defaultdict(list)
        for idx, point in zip(closestCentres, points):
            centrePoints[idx].append(point)
        # Move centres to the average position of their closest elements
        centres = map(averagePosition, centrePoints.itervalues())
    return centres


def recalculateCentres(centres, points, hiddenMatrix):
    """
    """
    denominators = map( lambda y : sum(map(lambda x : x[y], hiddenMatrix)), range(len(centres)))
    positions = map(lambda x: zip(*x) , [map( lambda point, matrix : [(pos * matrix[id])/denominators[id] for pos in point], points, hiddenMatrix) for id, centre in enumerate(centres)])
    newCentres = [map(sum, position) for position in positions]
    return newCentres

def softKMeanClustering(centres, points, beta, iterations=100):
    """
    Perform Soft k-Mean Clustering to calculate the location of the centres
    """
    for _ in range(iterations):
        elements = [map(lambda centre : exp(-1 * beta * distance(point, centre)), centres) for point in points]
        pointTotals = map(sum, elements)
        try:
            hiddenMatrix = map(lambda values, total : [v/total for v in values], elements, pointTotals)
            centres = recalculateCentres(centres, points, hiddenMatrix)
            'Print done'
        except ZeroDivisionError:
            print 'Attempt to divide by zero'
            print pointTotals
            raise
    
    return centres
    

def hierarchicalClustering(nodeIDs, distanceMatrix):
    """
    """
    while len(nodeIDs) > 1:
        i,j = findLowestElement(distanceMatrix)
        newNodeId = ' '.join([nodeIDs[i], nodeIDs[j]])
        
        # Calculate the Davg entry and add to the Distance Matrix
        for ptr in range(len(distanceMatrix)):
            distanceMatrix[ptr].append( ((distanceMatrix[ptr][i]) + (distanceMatrix[ptr][j]))/2.0)
        newElement = [(distanceMatrix[i][ptr] + distanceMatrix[j][ptr])/2.0 for ptr in range(len(distanceMatrix))]
        newElement.append(0)
        distanceMatrix.append(newElement)
        nodeIDs.append(newNodeId)
        del nodeIDs[j]
        del nodeIDs[i]
        distanceMatrix = removeEntry(removeEntry(distanceMatrix, j),i)
        yield newNodeId
    
if __name__ == '__main__':  # pragma: no cover
#     with open('data/farthestFirstTraversal_challenge.txt') as fp:
#         centreCount, _ = map(int, fp.readline().strip().split(' '))
#         points = readPoints(fp.readlines())
#         centres = farthestFirstTraversal(centreCount, points)
#         for centre in centres:
#             print ' '.join(map(str, centre))

    # Lloyd Algorithm
#     with open('data/lloydAlgorithm_challenge.txt') as fp:
#         centreCount, _ = map(int, fp.readline().strip().split(' '))
#         points = readPoints(fp.readlines())
#         centres = points[:centreCount]
#         centres = lloydAlgorithm(centres, points)
#         for centre in centres:
#             print ' '.join(map(lambda x:'{0:.3f}'.format(x), centre))

    # Soft K-Means Clustering
#     with open('data/kmeans_challenge.txt') as fp:
#         centreCount, _ = map(int, fp.readline().strip().split(' '))
#         beta = float(fp.readline().strip())
#         points = readPoints(fp.readlines())
#         centres = points[:centreCount]
#         centres = softKMeanClustering(centres, points, beta)
#         for centre in centres:
#             print ' '.join(map(lambda x:'{0:.3f}'.format(x), centre))
    
    
    # Hierarchical Clustering
    with open('data/hierarchicalClustering_extra.txt') as fp:
        nodeCount = int(fp.readline().strip())
        distanceMatrix = [map(float, line.split(' ')) for line in fp.readlines()]
        nodeIDs = map(str, range(1,nodeCount+1))
        
        for nodeId in hierarchicalClustering(nodeIDs, distanceMatrix):
            print nodeId
