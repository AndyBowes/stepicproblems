"""
Created on 28 Apr 2015

"""

from math import sqrt
import operator

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
    total = sum(map(pow(y=2), [min([distance(point, centre) for centre in centres]) for point in points]))
    return total / len(points)


if __name__ == '__main__':  # pragma: no cover
    with open('data/farthestFirstTraversal_challenge.txt') as fp:
        centreCount, _ = map(int, fp.readline().strip().split(' '))
        points = readPoints(fp.readlines())
        centres = farthestFirstTraversal(centreCount, points)
        for centre in centres:
            print ' '.join(map(str, centre))
