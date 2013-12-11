"""
Created on 10 Dec 2013
Coursera Chapter 6

"""
from collections import defaultdict
from heapq import heappop, heappush
from itertools import product

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
    dist = [[0 for x in xrange(width + 1)] for x in xrange(height + 1)]
    for x in xrange(1, width + 1):
        dist[x][0] = dist[x - 1][0] + right[x - 1][0]
    for y in xrange(1, height + 1):
        dist[0][y] = dist[0][y - 1] + down[0][y - 1]

    for x in xrange(1, width + 1):
        for y in xrange(1, height + 1):
            dist[x][y] = max([dist[x - 1][y] + down[x - 1][y - 1],
                              dist[x][y - 1] + right[x - 1][y - 1]])
    return dist[width][height]

if __name__ == '__main__':  # pragma: no cover
#    print dpChange(18996, [32, 22, 5, 3, 1])
#    longestCommonSubsequence('GATCTAAATGAGACTTCATTGCAAGCAGTTCTGAGACCAGATACCGCCGCAGAGAAGCCCCCGGATACTGTTTAGATGGCGTGCACTGGACGTGATGCAAAAGTGAGCAGCCGTCCGATTCATCATTAGGACTGAATATCTCTCAATCGAAGGCAGAGCTCCCTATGGCGCACAGGCCTACATATGCGCGTAGAGTTGCAGTGCATGTCTCAGTGTCGCTGCATGACATCTATCCCCACAGGTTCTCTTGGTTGATGGATGCCATAGCGGCAGCAATGTAGCATTTTCCTGGTGCGAAAGATCCTCCATAGAGCTGGCGATTGCCCTTGTCTCCTATACTTGAGGGGGACCGATCCCTGGAGGCTCGGAATAGGACGCCACTGTAGCGGCTGACTCGGACAAAAGCGCCGGAAGATCCTTGGCACCGATGCCACTTTGCCCTCGCTTAATAGCTACGTCCACGACCGCGAATGACTGGCGAATCTTTACTTGGTTTACCAAAATTTCGGAAAAGCGTGTGTTAGCATAACGGGCTAATTAAATTCGTTGACACATAGATGCACCCTCAACCCTTACAAAACGGGCGTCGGTTTGCAGAGGCAGCTAAAGGAGTGACAGTGGGGCCCGACTCACTATAAAGGGTAAAAGACGGGGACGTCTTAAACTTGGATACGCAAACAGGTGGATGGCCAGTTCAGTTGACCGTATGGCCATTGGTGGATCATACCACGACGACCGAAGATGTAATGGTATATAACGCCATGGCTACCCTTCTTAGATTCTTAACTGCAAGATCCAGTAATGCAGGTCTTACGCTGCTACGCTCCAAAAGAGACCATACTGGGTGTATGCTTACAGTGAAGATACCACTATTTGGTGCTCGCCAGATGGTTCTTCTGTGAATCGCGTCTAGTGACGACGTTTCATTTGCT',
# 'ATGTGGTGTTATCCCACCCCAGCGAATACTAGGTCTGTAGGGCGGTAGGACGTCACTGGGGGTCACACCTCATCGCACGACGCCTTGCATGTGGAGAATCGATCCTTTAGATTTCCGTGTACTCGGCCGAGTTGGTCGCACAGGGTAAAACGGTGGAAGTAAACTCAGAGATAGGGTGTTCTAAGTATATTTCTCGGCTCAGTGACCAAGACCCTCGTTGCCTCTATGCTACGGATTCGGGGGGCGTGATTCACTGTTCCCTCAGCAAAAGCGGCACCATCGGTGCGACTGGGCGCCACCGCTTACATCTAGCTGGGGCAGCGTACGTGACTACTCTGCGTATCTTTCGTAAACACGTATCATCAGTCCTAACGCGACTGATAGCCGTGCCTTAGGAAGCCTTCTGAGCTTCATTCCTAGGCTCGGCTCCGCAGATTGATATGTAAGCGCTTGAAAACACCCCTCGCGCGCTCCCCAGTCGACGTAAACAACTTCAAACCGATAGAACGCCACCTGGTGGCAGCTGGGTGGCTGCACTATACGGGGGTCAGGTATACACTTGCGTGCTACGTCTGGTGGTGAGTCGCGACAACAACCCTAATAGGTGGTGCCATCAGCCGCATTAATTAGGCGTGGATGCGTAGAACTTTGAAAGCCTGTCCTTGAGTACCCGGGGCCGAGAAGAGCAGCGTTTACTTCAAGTAAAGCAGGGTGGAACTATTGGGTGTCACCCACCCCAGTTGGTACGCAAGTTAAGATCTTCGGTAGAGTCGCCATCATTCAATTAATTAGTGATCGTCAGGCCTACGAACCGGATATGATAAC')
    print manhatten(4, 4, [[1, 0, 2, 4, 3], [4, 6, 5, 2, 1], [4, 4, 5, 2, 1], [5, 6, 8, 5, 3]],
                    [[3, 2, 4, 0], [3, 2, 4, 2], [0, 7, 3, 3], [3, 3, 0, 2], [1, 3, 2, 2]])
