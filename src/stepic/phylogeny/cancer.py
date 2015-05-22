'''
Created on 10 May 2015

@author: Andy
'''
from clustering import lloydAlgorithm, softKMeanClustering
import random

def _randomCentres(points, count):
    """
    Pick 
    """
    return random.sample(points, count)
    

def _readPositionsFile(inputFile):
    with open(inputFile) as fp:
        positions = [map(float, line.split(' ')) for line in fp.readlines()]
    return positions

def findClusterCentres(points, beta=2, clusterCount=8):
    """
    Find the location of 
    """
    centres = _randomCentres(points, clusterCount)
    for centre in centres:
        print centre
    centres = lloydAlgorithm(centres, points)
    print 'After Lloyd Algorithm'
    for centre in centres:
        print centre
        
    
#     centres = softKMeanClustering(centres, points, beta)
#     print 'After Soft Clustering'
#     for centre in centres:
#         print centre



if __name__ == '__main__':
    cancerPositions = _readPositionsFile('data/cancer/cancerous.txt')
    healthyPositions = _readPositionsFile('data/cancer/healthy.txt')
    
    centres = findClusterCentres(cancerPositions + healthyPositions,beta=0.01)
