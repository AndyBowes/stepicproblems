"""
Created on 10 Dec 2013
Coursera Chapter 6

"""
from collections import defaultdict
from heapq import heappop, heappush
from itertools import product, repeat
# pylint:disable=C0301, C0103

BLOSUM62 = {'A': {'A': 4, 'C': 0, 'E':-1, 'D':-2, 'G': 0, 'F':-2, 'I':-1, 'H':-2, 'K':-1, 'M':-1, 'L':-1, 'N':-2, 'Q':-1, 'P':-1, 'S': 1, 'R':-1, 'T': 0, 'W':-3, 'V': 0, 'Y':-2},
            'C': {'A': 0, 'C': 9, 'E':-4, 'D':-3, 'G':-3, 'F':-2, 'I':-1, 'H':-3, 'K':-3, 'M':-1, 'L':-1, 'N':-3, 'Q':-3, 'P':-3, 'S':-1, 'R':-3, 'T':-1, 'W':-2, 'V':-1, 'Y':-2},
            'E': {'A':-1, 'C':-4, 'E': 5, 'D': 2, 'G':-2, 'F':-3, 'I':-3, 'H': 0, 'K': 1, 'M':-2, 'L':-3, 'N': 0, 'Q': 2, 'P':-1, 'S': 0, 'R': 0, 'T':-1, 'W':-3, 'V':-2, 'Y':-2},
            'D': {'A':-2, 'C':-3, 'E': 2, 'D': 6, 'G':-1, 'F':-3, 'I':-3, 'H':-1, 'K':-1, 'M':-3, 'L':-4, 'N': 1, 'Q': 0, 'P':-1, 'S': 0, 'R':-2, 'T':-1, 'W':-4, 'V':-3, 'Y':-3},
            'G': {'A': 0, 'C':-3, 'E':-2, 'D':-1, 'G': 6, 'F':-3, 'I':-4, 'H':-2, 'K':-2, 'M':-3, 'L':-4, 'N': 0, 'Q':-2, 'P':-2, 'S': 0, 'R':-2, 'T':-2, 'W':-2, 'V':-3, 'Y':-3},
            'F': {'A':-2, 'C':-2, 'E':-3, 'D':-3, 'G':-3, 'F': 6, 'I': 0, 'H':-1, 'K':-3, 'M': 0, 'L': 0, 'N':-3, 'Q':-3, 'P':-4, 'S':-2, 'R':-3, 'T':-2, 'W': 1, 'V':-1, 'Y': 3},
            'I': {'A':-1, 'C':-1, 'E':-3, 'D':-3, 'G':-4, 'F': 0, 'I': 4, 'H':-3, 'K':-3, 'M': 1, 'L': 2, 'N':-3, 'Q':-3, 'P':-3, 'S':-2, 'R':-3, 'T':-1, 'W':-3, 'V': 3, 'Y':-1},
            'H': {'A':-2, 'C':-3, 'E': 0, 'D':-1, 'G':-2, 'F':-1, 'I':-3, 'H': 8, 'K':-1, 'M':-2, 'L':-3, 'N': 1, 'Q': 0, 'P':-2, 'S':-1, 'R': 0, 'T':-2, 'W':-2, 'V':-3, 'Y': 2},
            'K': {'A':-1, 'C':-3, 'E': 1, 'D':-1, 'G':-2, 'F':-3, 'I':-3, 'H':-1, 'K': 5, 'M':-1, 'L':-2, 'N': 0, 'Q': 1, 'P':-1, 'S': 0, 'R': 2, 'T':-1, 'W':-3, 'V':-2, 'Y':-2},
            'M': {'A':-1, 'C':-1, 'E':-2, 'D':-3, 'G':-3, 'F': 0, 'I': 1, 'H':-2, 'K':-1, 'M': 5, 'L': 2, 'N':-2, 'Q': 0, 'P':-2, 'S':-1, 'R':-1, 'T':-1, 'W':-1, 'V': 1, 'Y':-1},
            'L': {'A':-1, 'C':-1, 'E':-3, 'D':-4, 'G':-4, 'F': 0, 'I': 2, 'H':-3, 'K':-2, 'M': 2, 'L': 4, 'N':-3, 'Q':-2, 'P':-3, 'S':-2, 'R':-2, 'T':-1, 'W':-2, 'V': 1, 'Y':-1},
            'N': {'A':-2, 'C':-3, 'E': 0, 'D': 1, 'G': 0, 'F':-3, 'I':-3, 'H': 1, 'K': 0, 'M':-2, 'L':-3, 'N': 6, 'Q': 0, 'P':-2, 'S': 1, 'R': 0, 'T': 0, 'W':-4, 'V':-3, 'Y':-2},
            'Q': {'A':-1, 'C':-3, 'E': 2, 'D': 0, 'G':-2, 'F':-3, 'I':-3, 'H': 0, 'K': 1, 'M': 0, 'L':-2, 'N': 0, 'Q': 5, 'P':-1, 'S': 0, 'R': 1, 'T':-1, 'W':-2, 'V':-2, 'Y':-1},
            'P': {'A':-1, 'C':-3, 'E':-1, 'D':-1, 'G':-2, 'F':-4, 'I':-3, 'H':-2, 'K':-1, 'M':-2, 'L':-3, 'N':-2, 'Q':-1, 'P': 7, 'S':-1, 'R':-2, 'T':-1, 'W':-4, 'V':-2, 'Y':-3},
            'S': {'A': 1, 'C':-1, 'E': 0, 'D': 0, 'G': 0, 'F':-2, 'I':-2, 'H':-1, 'K': 0, 'M':-1, 'L':-2, 'N': 1, 'Q': 0, 'P':-1, 'S': 4, 'R':-1, 'T': 1, 'W':-3, 'V':-2, 'Y':-2},
            'R': {'A':-1, 'C':-3, 'E': 0, 'D':-2, 'G':-2, 'F':-3, 'I':-3, 'H': 0, 'K': 2, 'M':-1, 'L':-2, 'N': 0, 'Q': 1, 'P':-2, 'S':-1, 'R': 5, 'T':-1, 'W':-3, 'V':-3, 'Y':-2},
            'T': {'A': 0, 'C':-1, 'E':-1, 'D':-1, 'G':-2, 'F':-2, 'I':-1, 'H':-2, 'K':-1, 'M':-1, 'L':-1, 'N': 0, 'Q':-1, 'P':-1, 'S': 1, 'R':-1, 'T': 5, 'W':-2, 'V': 0, 'Y':-2},
            'W': {'A':-3, 'C':-2, 'E':-3, 'D':-4, 'G':-2, 'F': 1, 'I':-3, 'H':-2, 'K':-3, 'M':-1, 'L':-2, 'N':-4, 'Q':-2, 'P':-4, 'S':-3, 'R':-3, 'T':-2, 'W': 11, 'V':-3, 'Y': 2},
            'V': {'A': 0, 'C':-1, 'E':-2, 'D':-3, 'G':-3, 'F':-1, 'I': 3, 'H':-3, 'K':-2, 'M': 1, 'L': 1, 'N':-3, 'Q':-2, 'P':-2, 'S':-2, 'R':-3, 'T': 0, 'W':-3, 'V': 4, 'Y':-1},
            'Y': {'A':-2, 'C':-2, 'E':-2, 'D':-3, 'G':-3, 'F': 3, 'I':-1, 'H': 2, 'K':-2, 'M':-1, 'L':-1, 'N':-2, 'Q':-1, 'P':-3, 'S':-2, 'R':-2, 'T':-2, 'W': 2, 'V':-1, 'Y': 7}}

PAM250 = {'A': {'A': 2, 'C':-2, 'E': 0, 'D': 0, 'G': 1, 'F':-3, 'I':-1, 'H':-1, 'K':-1, 'M':-1, 'L':-2, 'N': 0, 'Q': 0, 'P': 1, 'S': 1, 'R':-2, 'T': 1, 'W':-6, 'V': 0, 'Y':-3},
          'C': {'A':-2, 'C': 12, 'E':-5, 'D':-5, 'G':-3, 'F':-4, 'I':-2, 'H':-3, 'K':-5, 'M':-5, 'L':-6, 'N':-4, 'Q':-5, 'P':-3, 'S': 0, 'R':-4, 'T':-2, 'W':-8, 'V':-2, 'Y': 0},
          'E': {'A': 0, 'C':-5, 'E': 4, 'D': 3, 'G': 0, 'F':-5, 'I':-2, 'H': 1, 'K': 0, 'M':-2, 'L':-3, 'N': 1, 'Q': 2, 'P':-1, 'S': 0, 'R':-1, 'T': 0, 'W':-7, 'V':-2, 'Y':-4},
          'D': {'A': 0, 'C':-5, 'E': 3, 'D': 4, 'G': 1, 'F':-6, 'I':-2, 'H': 1, 'K': 0, 'M':-3, 'L':-4, 'N': 2, 'Q': 2, 'P':-1, 'S': 0, 'R':-1, 'T': 0, 'W':-7, 'V':-2, 'Y':-4},
          'G': {'A': 1, 'C':-3, 'E': 0, 'D': 1, 'G': 5, 'F':-5, 'I':-3, 'H':-2, 'K':-2, 'M':-3, 'L':-4, 'N': 0, 'Q':-1, 'P': 0, 'S': 1, 'R':-3, 'T': 0, 'W':-7, 'V':-1, 'Y':-5},
          'F': {'A':-3, 'C':-4, 'E':-5, 'D':-6, 'G':-5, 'F': 9, 'I': 1, 'H':-2, 'K':-5, 'M': 0, 'L': 2, 'N':-3, 'Q':-5, 'P':-5, 'S':-3, 'R':-4, 'T':-3, 'W': 0, 'V':-1, 'Y': 7},
          'I': {'A':-1, 'C':-2, 'E':-2, 'D':-2, 'G':-3, 'F': 1, 'I': 5, 'H':-2, 'K':-2, 'M': 2, 'L': 2, 'N':-2, 'Q':-2, 'P':-2, 'S':-1, 'R':-2, 'T': 0, 'W':-5, 'V': 4, 'Y':-1},
          'H': {'A':-1, 'C':-3, 'E': 1, 'D': 1, 'G':-2, 'F':-2, 'I':-2, 'H': 6, 'K': 0, 'M':-2, 'L':-2, 'N': 2, 'Q': 3, 'P': 0, 'S':-1, 'R': 2, 'T':-1, 'W':-3, 'V':-2, 'Y': 0},
          'K': {'A':-1, 'C':-5, 'E': 0, 'D': 0, 'G':-2, 'F':-5, 'I':-2, 'H': 0, 'K': 5, 'M': 0, 'L':-3, 'N': 1, 'Q': 1, 'P':-1, 'S': 0, 'R': 3, 'T': 0, 'W':-3, 'V':-2, 'Y':-4},
          'M': {'A':-1, 'C':-5, 'E':-2, 'D':-3, 'G':-3, 'F': 0, 'I': 2, 'H':-2, 'K': 0, 'M': 6, 'L': 4, 'N':-2, 'Q':-1, 'P':-2, 'S':-2, 'R': 0, 'T':-1, 'W':-4, 'V': 2, 'Y':-2},
          'L': {'A':-2, 'C':-6, 'E':-3, 'D':-4, 'G':-4, 'F': 2, 'I': 2, 'H':-2, 'K':-3, 'M': 4, 'L': 6, 'N':-3, 'Q':-2, 'P':-3, 'S':-3, 'R':-3, 'T':-2, 'W':-2, 'V': 2, 'Y':-1},
          'N': {'A': 0, 'C':-4, 'E': 1, 'D': 2, 'G': 0, 'F':-3, 'I':-2, 'H': 2, 'K': 1, 'M':-2, 'L':-3, 'N': 2, 'Q': 1, 'P': 0, 'S': 1, 'R': 0, 'T': 0, 'W':-4, 'V':-2, 'Y':-2},
          'Q': {'A': 0, 'C':-5, 'E': 2, 'D': 2, 'G':-1, 'F':-5, 'I':-2, 'H': 3, 'K': 1, 'M':-1, 'L':-2, 'N': 1, 'Q': 4, 'P': 0, 'S':-1, 'R': 1, 'T':-1, 'W':-5, 'V':-2, 'Y':-4},
          'P': {'A': 1, 'C':-3, 'E':-1, 'D':-1, 'G': 0, 'F':-5, 'I':-2, 'H': 0, 'K':-1, 'M':-2, 'L':-3, 'N': 0, 'Q': 0, 'P': 6, 'S': 1, 'R': 0, 'T': 0, 'W':-6, 'V':-1, 'Y':-5},
          'S': {'A': 1, 'C': 0, 'E': 0, 'D': 0, 'G': 1, 'F':-3, 'I':-1, 'H':-1, 'K': 0, 'M':-2, 'L':-3, 'N': 1, 'Q':-1, 'P': 1, 'S': 2, 'R': 0, 'T': 1, 'W':-2, 'V':-1, 'Y':-3},
          'R': {'A':-2, 'C':-4, 'E':-1, 'D':-1, 'G':-3, 'F':-4, 'I':-2, 'H': 2, 'K': 3, 'M': 0, 'L':-3, 'N': 0, 'Q': 1, 'P': 0, 'S': 0, 'R': 6, 'T':-1, 'W': 2, 'V':-2, 'Y':-4},
          'T': {'A': 1, 'C':-2, 'E': 0, 'D': 0, 'G': 0, 'F':-3, 'I': 0, 'H':-1, 'K': 0, 'M':-1, 'L':-2, 'N': 0, 'Q':-1, 'P': 0, 'S': 1, 'R':-1, 'T': 3, 'W':-5, 'V': 0, 'Y':-3},
          'W': {'A':-6, 'C':-8, 'E':-7, 'D':-7, 'G':-7, 'F': 0, 'I':-5, 'H':-3, 'K':-3, 'M':-4, 'L':-2, 'N':-4, 'Q':-5, 'P':-6, 'S':-2, 'R': 2, 'T':-5, 'W': 17, 'V':-6, 'Y': 0},
          'V': {'A': 0, 'C':-2, 'E':-2, 'D':-2, 'G':-1, 'F':-1, 'I': 4, 'H':-2, 'K':-2, 'M': 2, 'L': 2, 'N':-2, 'Q':-2, 'P':-1, 'S':-1, 'R':-2, 'T': 0, 'W':-6, 'V': 4, 'Y':-2},
          'Y': {'A':-3, 'C': 0, 'E':-4, 'D':-4, 'G':-5, 'F': 7, 'I':-1, 'H': 0, 'K':-4, 'M':-2, 'L':-1, 'N':-2, 'Q':-4, 'P':-5, 'S':-3, 'R':-4, 'T':-3, 'W': 0, 'V':-2, 'Y': 10}}

DOWN = 1
RIGHT = 2
DIAG = 3
BACK = 4
START = 8
END = 16
HOME = -1

def dpChange(target, coins):
    """
    Calculate the minimum 
    """
    visited = defaultdict(lambda: False)
    stack = []
    heappush(stack, (0, 0))
    while stack:
        cnt, value = heappop(stack)
        if value == target:
            return cnt
        cnt += 1
        for c in coins:
            nextValue = value + c
            if nextValue <= target and visited[nextValue] == False:
                visited[nextValue] = True
                heappush(stack, (cnt, nextValue))

def longestCommonSubsequence(seq1, seq2):
    """
    Extract the longest common subsequence from 2 sequences
    """
    dp = defaultdict(str)
    for x, y in product(range(len(seq1)), range(len(seq2))):
        if seq1[x] == seq2[y]:
            dp[(x, y)] = dp[(x - 1, y - 1)] + seq1[x]
        else:
            dp[(x, y)] = max(dp[(x - 1, y)], dp[(x, y - 1)], key=len)
    print(dp[len(seq1) - 1, len(seq2) - 1])

def manhatten(width, height, down, right):
    """
    Perform a Manhatten walk to get the max possible value in last element
    """
    dist = [[0 for _ in xrange(width + 1)] for _ in xrange(height + 1)]
    for i in range(1, width + 1):
        dist[0][i] = dist[0][i - 1] + right[0][i - 1]
    for i in range(1, height + 1):
        dist[i][0] = dist[i - 1][0] + down[i - 1][0]
    for x in xrange(1, width + 1):
        for y in xrange(1, height + 1):
            dist[y][x] = max([dist[y - 1][x] + down[y - 1][x],
                                  dist[y][x - 1] + right[y][x - 1]])
    return dist[height][width]

def longestPath(start, finish, nodes):
    """
    Find the longest path between the Start Node and the Finish Node
    Return the sum of the distances plus the path from the source to the finish
    """
    # Visited Dict : Key = NodeId, value = (totalWeight, previousNode)
    visited = defaultdict(lambda: (0, None))
    stack = []
    # Push element onto Stack with the following properties pathLength, nodeId, totalWeight
    heappush(stack, (0, start, 0))
    while stack:
        dist, id, pathWeight = heappop(stack)
        # Fetch children of id & add to queue if dist + weight > current value:
        for childId, weight in nodes[id]:
            if pathWeight + weight > visited[childId][0]:
                visited[childId] = (pathWeight + weight, id)
                heappush(stack, (dist + 1, childId, pathWeight + weight))
    # Need to Backtrack
    path = [finish]
    id = finish
    while id != start:
        id = visited[id][1]
        path.append(id)
    return (visited[finish][0], reversed(path))

def globalAlignment(sequence1, sequence2, scoringMatrix=None, indelPenalty=5):
    """
    Perform a Global Alignment between 2 Sequences
    Return the best score and the 2 Aligned Sequences
    """
    if scoringMatrix == None:
        scoringMatrix = BLOSUM62

    s1Length = len(sequence1)
    s2Length = len(sequence2)
    score = [[(-i * indelPenalty, DOWN)] + list(repeat((0, 0), s1Length)) for i in range(s2Length + 1)]
    for i in range(1, s1Length + 1):
        score[0][i] = (-i * indelPenalty, RIGHT)
    score[0][0] = (0, HOME)

    for x in xrange(1, s1Length + 1):
        for y in xrange(1, s2Length + 1):
            cellScores = [ (score[y - 1][x - 1][0] + scoringMatrix[sequence1[x - 1]][sequence2[y - 1]], DIAG),
                           (score[y][x - 1][0] - indelPenalty, RIGHT),
                           (score[y - 1][x][0] - indelPenalty, DOWN)]
            score[y][x] = max(cellScores, key=lambda t: t[0])

    x = s1Length
    y = s2Length
    align1 = ''
    align2 = ''
    bestScore = score[s2Length][s1Length][0]
    while x > 0 or y > 0:
        dir = score[y][x][1]
        if dir == DIAG:
            x -= 1
            y -= 1
            align1 = sequence1[x] + align1
            align2 = sequence2[y] + align2
        if dir == DOWN:
            y -= 1
            align1 = '-' + align1
            align2 = sequence2[y] + align2
        if dir == RIGHT:
            x -= 1
            align1 = sequence1[x] + align1
            align2 = '-' + align2
    return bestScore, align1, align2


def localAlignment(sequence1, sequence2, scoringMatrix=None, indelPenalty=5):
    """
    Perform a Local Alignment between 2 Sequences
    Return the best score and the 2 Aligned Sequences
    """
    if scoringMatrix == None:
        scoringMatrix = PAM250

    s1Length = len(sequence1)
    s2Length = len(sequence2)
    score = [[(0, DOWN)] + list(repeat((0, 0), s1Length)) for i in range(s2Length + 1)]
    for i in range(1, s1Length + 1):
        score[0][i] = (0, RIGHT)
    score[0][0] = (0, HOME)

    bestScore = 0
    maxLocation = None
    for x in xrange(1, s1Length + 1):
        for y in xrange(1, s2Length + 1):
            cellScores = [ (0, HOME),
                           (score[y - 1][x - 1][0] + scoringMatrix[sequence1[x - 1]][sequence2[y - 1]], DIAG),
                           (score[y][x - 1][0] - indelPenalty, RIGHT),
                           (score[y - 1][x][0] - indelPenalty, DOWN)]
            score[y][x] = max(cellScores, key=lambda t: t[0])
            if score[y][x][0] > bestScore:
                bestScore = score[y][x][0]
                maxLocation = (y, x)

    align1, align2 = _backtrackAlignment((maxLocation[1], maxLocation[0]), score, sequence1, sequence2)
    return bestScore, align1, align2


def _backtrackAlignment(start, score, sequence1, sequence2):
    """
    Backtrack from the start point to HOME 
    """
    x = start[0]
    y = start[1]
    align1 = ''
    align2 = ''
    while score[y][x][1] != HOME:
        dir = score[y][x][1]
        if dir == DIAG:
            x -= 1
            y -= 1
            align1 = sequence1[x] + align1
            align2 = sequence2[y] + align2
        if dir == DOWN:
            y -= 1
            align1 = '-' + align1
            align2 = sequence2[y] + align2
        if dir == RIGHT:
            x -= 1
            align1 = sequence1[x] + align1
            align2 = '-' + align2
    return align1, align2


def editDistance(sequence1, sequence2):
    """
    Calculate the minimum Edit Distance between 2 sequences
    """
    s1Length = len(sequence1)
    s2Length = len(sequence2)
    score = [ [i] + list(repeat(0, s1Length)) for i in range(s2Length + 1)]
    for i in range(1, s1Length + 1):
        score[0][i] = i

    for x in xrange(1, s1Length + 1):
        for y in xrange(1, s2Length + 1):
            cellScores = [ score[y - 1][x - 1] + (0 if sequence1[x - 1] == sequence2[y - 1] else 1),
                           score[y][x - 1] + 1,
                           score[y - 1][x] + 1]
            score[y][x] = min(cellScores)
    return score[s2Length][s1Length]

def fittingAlignment(sequence1, sequence2):
    """
    Fitting Alignment
    Find local alignment of sequence2 within sequence1. There is zero penalty at either end
    of sequence2.
    Just need to find the max score at the end of sequence2 to locate the last 
    """
    s1Length = len(sequence1)
    s2Length = len(sequence2)
    score = [[(-i, DOWN)] + list(repeat((0, 0), s1Length)) for i in range(s2Length + 1)]
    for i in range(1, s1Length + 1):
        score[0][i] = (0, HOME)
    score[0][0] = (0, HOME)

    for x in xrange(1, s1Length + 1):
        for y in xrange(1, s2Length + 1):
            diagScore = 1 if sequence1[x - 1] == sequence2[y - 1] else -1
#             cellScores = [ (score[y][x - 1][0] - 1, RIGHT),
#                            (score[y - 1][x][0] - 1, DOWN),
#                            (score[y - 1][x - 1][0] + diagScore, DIAG),
#                            (0, HOME)]
            cellScores = [ (score[y - 1][x - 1][0] + diagScore, DIAG),
                           (score[y][x - 1][0] - 1, RIGHT),
                           (score[y - 1][x][0] - 1, DOWN)
                           ]
            score[y][x] = max(cellScores, key=lambda t: t[0])

    bestCell = max(enumerate(score[-1]), key=lambda t : t[1][0])
    start = (bestCell[0], s2Length)
    bestscore = bestCell[1][0]
    align1, align2 = _backtrackAlignment(start, score, sequence1, sequence2)
    return bestscore, align1, align2



def overlapAlignment(sequence1, sequence2):
    """
    Overlap Alignment take the end of 1 sequence and the start of the other
    There is a zero penalty at the start of 1 string and a zero penalty at the end of the other.    
    """
    s1Length = len(sequence1)
    s2Length = len(sequence2)
    score = [[(-i * 2, DOWN)] + list(repeat((0, 0), s1Length)) for i in range(s2Length + 1)]
    for i in range(1, s1Length + 1):
        score[0][i] = (0, HOME)
    score[0][0] = (0, HOME)

    for x in xrange(1, s1Length + 1):
        for y in xrange(1, s2Length + 1):
            diagScore = 1 if sequence1[x - 1] == sequence2[y - 1] else -2
#             cellScores = [ (score[y][x - 1][0] - 1, RIGHT),
#                            (score[y - 1][x][0] - 1, DOWN),
#                            (score[y - 1][x - 1][0] + diagScore, DIAG),
#                            (0, HOME)]
            cellScores = [ (score[y - 1][x - 1][0] + diagScore, DIAG),
                           (score[y][x - 1][0] - 2, RIGHT),
                           (score[y - 1][x][0] - 2, DOWN)]
            score[y][x] = max(cellScores, key=lambda t: t[0])

    bestscore = -1
    bestY = -1
    for i in range(1, s2Length):
        if score[i][-1][0] > bestscore:
            bestscore = score[i][-1][0]
            bestY = i

    start = (s1Length, bestY)
    align1, align2 = _backtrackAlignment(start, score, sequence1, sequence2)
    return bestscore, align1, align2


def affineAlignment(sequence1, sequence2, indelPenalty=1, openPenalty=11, scoringMatrix=None):
    """
    Perform a Global Alignment between 2 Sequences with Affine Gap Penalties
    Return the best score and the 2 Aligned Sequences
    """
    if scoringMatrix == None:
        scoringMatrix = BLOSUM62

    s1Length = len(sequence1)
    s2Length = len(sequence2)
    score = [[(-i * indelPenalty, DOWN)] + list(repeat((0, 0), s1Length)) for i in range(s2Length + 1)]
    for i in range(1, s1Length + 1):
        score[0][i] = (-i * indelPenalty, RIGHT)
    score[0][0] = (0, HOME)

    for x in xrange(1, s1Length + 1):
        for y in xrange(1, s2Length + 1):
            rightPenalty = indelPenalty if score[y][x - 1][1] == RIGHT else openPenalty
            downPenalty = indelPenalty if score[y - 1][x][1] == DOWN else openPenalty
            cellScores = [ (score[y - 1][x - 1][0] + scoringMatrix[sequence1[x - 1]][sequence2[y - 1]], DIAG),
                           (score[y][x - 1][0] - rightPenalty, RIGHT),
                           (score[y - 1][x][0] - downPenalty, DOWN)]
            score[y][x] = max(cellScores, key=lambda t: t[0])

    bestScore = score[s2Length][s1Length][0]
    start = (s1Length, s2Length)
    align1, align2 = _backtrackAlignment(start, score, sequence1, sequence2)
    return bestScore, align1, align2

def findMiddleEdge(sequence1, sequence2, indelPenalty=1, openPenalty=11, scoringMatrix=None):
    """
    Perform a Global Alignment between 2 Sequences with Affine Gap Penalties
    Return the best score and the 2 Aligned Sequences
    """
    if scoringMatrix == None:
        scoringMatrix = BLOSUM62

    s1Length = len(sequence1)
    s2Length = len(sequence2)
    score = [[(-i * indelPenalty, DOWN)] + list(repeat((0, 0), s1Length)) for i in range(s2Length + 1)]
    for i in range(1, s1Length + 1):
        score[0][i] = (-i * indelPenalty, RIGHT)
    score[0][0] = (0, HOME)

    for x in xrange(1, s1Length + 1):
        for y in xrange(1, s2Length + 1):
            rightPenalty = indelPenalty if score[y][x - 1][1] == RIGHT else openPenalty
            downPenalty = indelPenalty if score[y - 1][x][1] == DOWN else openPenalty
            cellScores = [ (score[y - 1][x - 1][0] + scoringMatrix[sequence1[x - 1]][sequence2[y - 1]], DIAG),
                           (score[y][x - 1][0] - rightPenalty, RIGHT),
                           (score[y - 1][x][0] - downPenalty, DOWN)]
            score[y][x] = max(cellScores, key=lambda t: t[0])

    def doBackTrack(s1Length, s2Length, score):
        x = s1Length
        y = s2Length
        while y > s2Length / 2:
            dir = score[y][x][1]
            if dir == DIAG:
                x -= 1
                y -= 1
            if dir == DOWN:
                y -= 1
            if dir == RIGHT:
                x -= 1
            yield (x, y)

    route = list(doBackTrack(s1Length, s2Length, score))
    return route[-1], route[-2]

def multipleSequenceAlignment(sequence1, sequence2, sequence3):
    s1Length = len(sequence1)
    s2Length = len(sequence2)
    s3Length = len(sequence3)

    score = [[[(0, DOWN)] + list(repeat((0, DOWN), s1Length)) for i in range(s2Length + 1)] for j in range(s3Length + 1)]
    for i in range(1, s1Length + 1):
        for j in range(1, s2Length + 1):
            score[0][j][i] = (0, DOWN + RIGHT)
    for i in range(1, s2Length + 1):
        for j in range(1, s3Length + 1):
            score[j][i][0] = (0, BACK + RIGHT)
    for i in range(1, s1Length + 1):
        for j in range(1, s3Length + 1):
            score[j][0][i] = (0, BACK + DOWN)
    for i in range(1, s2Length + 1):
        score[0][i][0] = (0, RIGHT)
    for i in range(1, s3Length + 1):
        score[i][0][0] = (0, BACK)
    score[0][0][0] = (0, HOME)

    for x in xrange(1, s1Length + 1):
        for y in xrange(1, s2Length + 1):
            for z in xrange(1, s3Length + 1):
                cellScores = []
                diagScore = 1 if (sequence1[x - 1] == sequence2[y - 1] and sequence1[x - 1] == sequence3[z - 1]) else 0
                cellScores.append((score[z - 1][y - 1][x - 1][0] + diagScore, 7))
                for direction in [6, 5, 3, 4, 2, 1]:
                    deltaZ = -1 if direction & BACK > 0 else 0
                    deltaY = -1 if direction & RIGHT > 0 else 0
                    deltaX = -1 if direction & DOWN > 0 else 0
                    cellScores.append((score[z + deltaZ][y + deltaY][x + deltaX][0], direction))
                score[z][y][x] = max(cellScores, key=lambda t: t[0])

    x = s1Length
    y = s2Length
    z = s3Length
    bestScore = score[z][y][x][0]
    align1, align2, align3 = '', '', ''
    while score[z][y][x][1] != HOME:
        direction = score[z][y][x][1]
        if direction & DOWN > 0:
            align1 = sequence1[x - 1] + align1
            x -= 1
        else:
            align1 = '-' + align1
        if direction & RIGHT > 0:
            align2 = sequence2[y - 1] + align2
            y -= 1
        else:
            align2 = '-' + align2
        if direction & BACK > 0:
            align3 = sequence3[z - 1] + align3
            z -= 1
        else:
            align3 = '-' + align3

    return bestScore, align1, align2, align3

if __name__ == '__main__':  # pragma: no cover
    print dpChange(18884, [1, 3, 5, 7, 8, 9, 18, 19, 20])
#    longestCommonSubsequence('GATCTAAATGAGACTTCATTGCAAGCAGTTCTGAGACCAGATACCGCCGCAGAGAAGCCCCCGGATACTGTTTAGATGGCGTGCACTGGACGTGATGCAAAAGTGAGCAGCCGTCCGATTCATCATTAGGACTGAATATCTCTCAATCGAAGGCAGAGCTCCCTATGGCGCACAGGCCTACATATGCGCGTAGAGTTGCAGTGCATGTCTCAGTGTCGCTGCATGACATCTATCCCCACAGGTTCTCTTGGTTGATGGATGCCATAGCGGCAGCAATGTAGCATTTTCCTGGTGCGAAAGATCCTCCATAGAGCTGGCGATTGCCCTTGTCTCCTATACTTGAGGGGGACCGATCCCTGGAGGCTCGGAATAGGACGCCACTGTAGCGGCTGACTCGGACAAAAGCGCCGGAAGATCCTTGGCACCGATGCCACTTTGCCCTCGCTTAATAGCTACGTCCACGACCGCGAATGACTGGCGAATCTTTACTTGGTTTACCAAAATTTCGGAAAAGCGTGTGTTAGCATAACGGGCTAATTAAATTCGTTGACACATAGATGCACCCTCAACCCTTACAAAACGGGCGTCGGTTTGCAGAGGCAGCTAAAGGAGTGACAGTGGGGCCCGACTCACTATAAAGGGTAAAAGACGGGGACGTCTTAAACTTGGATACGCAAACAGGTGGATGGCCAGTTCAGTTGACCGTATGGCCATTGGTGGATCATACCACGACGACCGAAGATGTAATGGTATATAACGCCATGGCTACCCTTCTTAGATTCTTAACTGCAAGATCCAGTAATGCAGGTCTTACGCTGCTACGCTCCAAAAGAGACCATACTGGGTGTATGCTTACAGTGAAGATACCACTATTTGGTGCTCGCCAGATGGTTCTTCTGTGAATCGCGTCTAGTGACGACGTTTCATTTGCT',
# 'ATGTGGTGTTATCCCACCCCAGCGAATACTAGGTCTGTAGGGCGGTAGGACGTCACTGGGGGTCACACCTCATCGCACGACGCCTTGCATGTGGAGAATCGATCCTTTAGATTTCCGTGTACTCGGCCGAGTTGGTCGCACAGGGTAAAACGGTGGAAGTAAACTCAGAGATAGGGTGTTCTAAGTATATTTCTCGGCTCAGTGACCAAGACCCTCGTTGCCTCTATGCTACGGATTCGGGGGGCGTGATTCACTGTTCCCTCAGCAAAAGCGGCACCATCGGTGCGACTGGGCGCCACCGCTTACATCTAGCTGGGGCAGCGTACGTGACTACTCTGCGTATCTTTCGTAAACACGTATCATCAGTCCTAACGCGACTGATAGCCGTGCCTTAGGAAGCCTTCTGAGCTTCATTCCTAGGCTCGGCTCCGCAGATTGATATGTAAGCGCTTGAAAACACCCCTCGCGCGCTCCCCAGTCGACGTAAACAACTTCAAACCGATAGAACGCCACCTGGTGGCAGCTGGGTGGCTGCACTATACGGGGGTCAGGTATACACTTGCGTGCTACGTCTGGTGGTGAGTCGCGACAACAACCCTAATAGGTGGTGCCATCAGCCGCATTAATTAGGCGTGGATGCGTAGAACTTTGAAAGCCTGTCCTTGAGTACCCGGGGCCGAGAAGAGCAGCGTTTACTTCAAGTAAAGCAGGGTGGAACTATTGGGTGTCACCCACCCCAGTTGGTACGCAAGTTAAGATCTTCGGTAGAGTCGCCATCATTCAATTAATTAGTGATCGTCAGGCCTACGAACCGGATATGATAAC')
#    print manhatten(4, 4, [[1, 0, 2, 4, 3], [4, 6, 5, 2, 1], [4, 4, 5, 2, 1], [5, 6, 8, 5, 3]],
#                    [[3, 2, 4, 0], [3, 2, 4, 2], [0, 7, 3,u 3], [3, 3, 0, 2], [1, 3, 2, 2]])

#    print longestPath(0, 4, {0:[(1, 7), (2, 4)], 2:[(3, 2)], 1:[(4, 1)], 3:[(4, 3)], 4:[]})
#    print globalAlignment('MNCNDDNFLYFMEHITTQEVYWFMSCAVLGQRGWKCNHFSAADPVPYLPHCHRDSGGQEAFNVVMLQAFLNFNIHEFWTDSMCRGGRQRNAHQTHATRFFKQIHMDCMVTAIFWCKMLAVYPLLYQGIQSTAHCTEPYLSKKMKMYEAFMLKMYKICKHKPDHFTEPDVRVLPESLVMPTTRKTYCPCKKPQKSRRMHMRALGEFKWPDMGSYQETQTEHWGYNWLPEQSTRKYIVQRCEVCEYMSNAAKIGQLSEHNENWPIVLAYQVREVGLAEMFTDLSWFVGHDWLGVTQRWDLWDPINWMNMLFPDDRAEYIYNCWCIRYSRYGPETYCFTTFSVGMHGCEMKQSGKGLPKDLSAFVIQHYVPILKRTPLQWGWPMRSGENREWGVNFKSCFMIWMSEFFTDPRASPIRVLSIWSKIHQQILLLNLNYEIMMYYSPWHVWKWQAESKLRCIIEVRPSGMIQMPDAAYIMIFNLQKFLSIFSDSQLFNIECHLDPGGMMEPPSIQKFSMIHNFAEKMHRMNLENKVDSLYCDSQGMTHKNLGMNVHAKHGKPYNSLNYIPQMCDFMFKDRQTMCAMYPLTQDPSFQRKRNQPCFARHHLENRRNFPTQNAIFPAYEMTGSVIMFPETVRPFQADSDYWYWDQKFREAQTFVVLSATSALRTQKQTWVGEYDKEKKRQPIWQEGFLHVIFCFVHMVMCQNAAWGNFRPLMGSHVCYIESISCDQNYGDVREAPSMWIDHHSEISGINTFAMEWQSGHEAIQCIVTANTHMSEFPHIGMDIS',
#                          'MFDNDDNFLYFMEHKHFNKMPNCTTFEKRLSAEVYWFMSCRALSNRGWDCNHNEMKDMIAKSAAHRDSGGQEAFNVVYYQAFLNFNIHEFWTDSMCRGWRPNHRNAHENKQAKTNRWHATREFKHMDCKMLAVYPLLPQGIQSTAHCTVPCPYLSGKEKMYEAFMLKMDKNLGKTNQNLHSIRNRDVRVLPESLVMPTTRCPCKKPQKAMYFARRMHMRALGEFKFPDMNSYQETQTEHWGYNGYLGGNILSTRKYIVQDCGVCEYMSNAAKIGQLSEINENWPIVLAYQVCEIMLKNCAMFTLGVTVKWDPHQWDMINWMNMFFPKRDRAEMISEVWPGYGSVGMHGHRHVQMNPFEMKQSGILLAPIRNGLPKDLSAFVIPYLKRTPLQWMKPMMPNWDLKQNWWIAMRSCFMIWMSYFVTDPTLRSPIRVLSIWSKIHQQMRLLLNLNYEIMMYYSPWRPPHYKVWKWQIVESKLRCIIEIREGMIQTPDAAYIMVIWYNMPNFNLKFLAIFSDNQYVWMRKVIFNIECHLDHGGMMEPLSEFTLRWFIQKFMHRMNGCDSQGMTHKNLHYRKPYNSLNYIPQMCDNMFKHLIYWYEQTPLTQDPSFERKQNQPCFARHHLEQYGRNVFFYLPPIQNAFFPAYEMAGSVIMFPETVRPFYWYQELRLQTFVVLDATSALRTQKQTWFGIYDKLKRQPIWQEGFLHVIFKMVHMVMCQNAAWGNFRPLMGSHVCYIELSICVNMWFFLICDQNYVDVRHAHEQQHSEISGINTFADEWQSSSHEAIQYIGLQIRTHMSEFPFTIGMHQVDYSS')
#     sc, align1, align2 = affineAlignment('PRTEINS', 'PRTWPSEIN')
#     print sc
#     print align1
#     print align2
#    print findMiddleEdge('PLEASANTLY', 'MEASNLY')
#    sc, a1, a2, a3 = multipleSequenceAlignment('ATATCCG', 'TCCGA', 'ATGTACTG')
#    print sc
#    print a1
#    print a2
#    print a3
