"""
Created on 29 Nov 2013

"""

from collections import defaultdict

def findEulerTour(graph):
    tour = []
    edges = graph

    numEdges = defaultdict(int)

    def findTour(u):
        for e in edges:
            if u == e[0]:
                u, v = e
                edges.remove(e)
                findTour(v)
            elif u == e[1]:
                v, u = e
                edges.remove(e)
                findTour(v)
        tour.insert(0, u)

    for i, j in graph:
        numEdges[i] += 1
        numEdges[j] += 1

    start = graph[0][0]
    for i, j in numEdges.iteritems():
        if j % 2 > 0:
            start = i
            break

    current = start
    find_tour(current)

    if tour[0] != tour[-1]:
        return None
    return tour


if __name__ == '__main__':  # pragma: no cover
    pass
