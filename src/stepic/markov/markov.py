'''
Created on 21 May 2015

@author: Andy Bowes
'''
from math import log
from stepic.motif import constructProbabilityProfile
from itertools import product
from collections import defaultdict

import operator

def calcPathProbability(alphabet, path, transitionMatrix):
    """
    This assumes that the probability of the initial state is just 1/n
    """
    return reduce(lambda x, y: x * transitionMatrix[path[y]][path[y+1]],
                xrange(len(path)-1),
                1.0/len(alphabet))
    
def calcEmissionPathProbability(alphabet, path, hiddenPath, emissionMatrix):
    """
    """
    return reduce(lambda x, y: x * emissionMatrix[hiddenPath[y]][path[y]],
                xrange(len(path)),
                1.0)

def readEmissionProbabilityInputFile(filePath):
    """
    """
    with open(filePath) as fp:
        path = fp.readline().strip()
        fp.readline()
        alphabet = fp.readline().strip().split(' ')
        fp.readline()
        hiddenModel = fp.readline().strip()
        fp.readline()
        fp.readline()
        fp.readline()
        fp.readline()
        emissionMatrix = {}
        for line in fp.readlines():
            elements = line.strip().split('\t')
            key = elements[0]
            values = elements[1:]
            emissionMatrix[key] = {k : v for k, v in zip(alphabet, map(float, values))}
    return alphabet, path, hiddenModel, emissionMatrix

    
    
def readPathProbabilityInputFile(filePath):
    """
    """
    with open(filePath) as fp:
        path = fp.readline().strip()
        fp.readline()
        alphabet = fp.readline().strip().split(' ')
        fp.readline()
        fp.readline()
        transitionMatrix = {}
        for line in fp.readlines():
            elements = line.strip().split('\t')
            key = elements[0]
            values = elements[1:]
            transitionMatrix[key] = {k : v for k, v in zip(alphabet, map(float, values))}
    return alphabet, path, transitionMatrix


def readViterbiInputFile(filePath):
    """
    Extract the information from the Viterbi Input File
    """
    with open(filePath) as fp:
        path = fp.readline().strip()
        fp.readline()
        alphabet = fp.readline().strip().split(' ')
        fp.readline()
        states = fp.readline().strip().split(' ')
        fp.readline()
        fp.readline()
        transmissionMatrix = {}
        for _ in xrange(len(states)):
            elements = fp.readline().strip().split('\t')
            key = elements[0]
            values = elements[1:]
            transmissionMatrix [key] = {k : v for k, v in zip(states, map(float, values))}
        fp.readline()
        fp.readline()
        emissionMatrix = {}
        for line in fp.readlines():
            elements = line.strip().split('\t')
            key = elements[0]
            values = elements[1:]
            emissionMatrix[key] = {k : v for k, v in zip(alphabet, map(float, values))}
    return path, alphabet, states, transmissionMatrix, emissionMatrix


def viterbi(path, alphabet, states, transitionMatrix, emissionMatrix):
    """
    Perform the Viterbi Algorithm to identify the most likely Hidden Markov Model. 
    
    [NB - Use logs rather than multiplication of small numbers]
    """

    def characterScore(fromState, toState, emittedChar, previousScores):
        return previousScores[fromState][0] + log(transitionMatrix[fromState][toState]*emissionMatrix[toState][emittedChar])
        
    graph = [{ state : (0, '') for state in states}]
    
    # Go through t
    for n in xrange(len(path)):
        emittedChar = path[n]
        previousScores = graph[-1]
        
        newScores = { toState : max(map(lambda fromState: (characterScore(fromState, toState, emittedChar, previousScores),fromState), states), key=lambda t: t[0])
                                for toState in states }
        graph.append(newScores)
    
    # Back track through the results to identify the most probable path by following the thread through the matrix
    # State at most probable state in final column.
    hiddenChar = max(graph[-1].iteritems(), key=operator.itemgetter(1))[0]
    hmm = ''
    n = len(path)
    while n > 0:
        hmm = hiddenChar + hmm
        hiddenChar = graph[n][hiddenChar][1]
        n = n - 1
    return hmm

def hmmProbability(path, alphabet, states, transitionMatrix, emissionMatrix):
    """
    Calculate the probability of the path occurring given the transition & emission matrices.
    Assumes that all of the initial starts are equally likely
    """
    
    def characterScore(fromState, toState, emittedChar, previousScores):
        return previousScores[fromState] * transitionMatrix[fromState][toState] * emissionMatrix[toState][emittedChar]
        
    graph = [{ state : 1.0/len(states) * emissionMatrix[state][path[0]] for state in states}]
    
    # Go through t
    for n in xrange(1,len(path)):
        emittedChar = path[n]
        previousScores = graph[-1]
        newScores = {toState : sum(map(lambda fromState: characterScore(fromState, toState, emittedChar, previousScores), states )) for toState in states }
        graph.append(newScores)

    return sum(graph[-1].itervalues())


def readHmmProfileFile(filePath):
    """
    """
    with open(filePath) as fp:
        threshold = float(fp.readline().strip())
        fp.readline()
        alphabet = fp.readline().strip().split(' ')
        fp.readline()
        alignments = [line.strip() for line in fp.readlines()]
    return threshold, alphabet, alignments
    
def readHmmProfileWithPseudoCountFile(filePath):
    """
    """
    with open(filePath) as fp:
        threshold, pseudoCount = map(float, fp.readline().strip().split())
        fp.readline()
        alphabet = fp.readline().strip().split(' ')
        fp.readline()
        alignments = [line.strip() for line in fp.readlines()]
    return threshold, alphabet, alignments, pseudoCount

def readHmmSequenceAlignmentFile(filePath):
    """
    """
    with open(filePath) as fp:
        sequence = fp.readline().strip()
        fp.readline()
        threshold, pseudoCount = map(float, fp.readline().strip().split())
        fp.readline()
        alphabet = fp.readline().strip().split(' ')
        fp.readline()
        alignments = [line.strip() for line in fp.readlines()]
    return threshold, alphabet, alignments, pseudoCount, sequence
    
    
    
def hmmProfile(threshold,alphabet,alignments,pseudoCount=0):
    """
    Calculate the HMM Profile
    Ignore columns where the number of insertions exceeds the threshold.
    """
    insertionCounts = map(lambda y : sum(1 for i in y if i == '-') , map( lambda x: x ,zip(*alignments)))
    noOfSequences = float(len(alignments))
    seedColumnIndicator = map(lambda y : y < threshold, map(lambda x: x/noOfSequences, insertionCounts))
    # Strip elements whose insertions ratio > threshold
    reducedAlignments = map(lambda alignment:''.join([x for x, y in zip(alignment, seedColumnIndicator) if y]), alignments)
    
    noOfSeedColumns = len(reducedAlignments[0])
    states = ['S','I0']  +  map(lambda x: x[1]+x[0] ,  product(map(str, xrange(1,noOfSeedColumns+1)),'MDI'))  + ['E']

    transitionCounts = {s: defaultdict(int) for s in states}
    emissionCounts = {s: defaultdict(int) for s in states}

    for alignment in alignments:
        fromState = 'S'
        seedColumnIndex = 0
        for i in xrange(len(alignment)):
            currentChar = alignment[i]
            if seedColumnIndicator[i]:
                seedColumnIndex += 1
                if currentChar == '-':
                    toState = 'D' + str(seedColumnIndex)
                else:
                    toState = 'M' + str(seedColumnIndex)
            else:
                if currentChar == '-':
                    continue
                else:
                    toState = 'I' + str(seedColumnIndex)
            emissionCounts[toState][currentChar] += 1
            transitionCounts[fromState][toState] += 1
            fromState = toState
        transitionCounts[fromState]['E'] += 1

    def itemValue(value,total):
        return 0 if value == 0 else float(value)/total

    transitionMatrix = {}
    for s in states:
        stateTotal = float(sum(transitionCounts[s].itervalues()))
        transitionMatrix[s] = { s2: itemValue(transitionCounts[s][s2], stateTotal) for s2 in states}

    emissionMatrix = {}
    for s in states:
        stateTotal = sum(emissionCounts[s].itervalues())
        emissionMatrix[s] = { a: itemValue(emissionCounts[s][a], stateTotal) for a in alphabet}


    def getNextStates(state, states, lastColumn):
        prefix = state[0]
        if prefix == 'S':
            return ['I0','M1','D1']
        if prefix == 'E':
            return []

        colCount = int(state[1:])
        if prefix in ['I','M','D']:
            if colCount >= lastColumn:
                return ['I{0}'.format(colCount), 'E']
            else:
                return ['I{0}'.format(colCount), 'M{0}'.format(colCount+1),'D{0}'.format(colCount+1)]
        else:
            return []

    def rebaseElements(elements):
        total = sum(elements.itervalues())
        return {k: v/total for k,v in elements.iteritems()}

    if pseudoCount > 0:
        for state in states:
            nextStates = getNextStates(state, states, noOfSeedColumns)
            if len(nextStates) > 0:
                for nextState in nextStates:
                    transitionMatrix[state][nextState] += pseudoCount
                transitionMatrix[state] = rebaseElements(transitionMatrix[state])
                    
        for state in states:
            if state[0] in ['I','M']:
                emissionMatrix[state] = rebaseElements({ k: v + pseudoCount for k,v in emissionMatrix[state].iteritems()})

    
    def printTable(xAxis,yAxis,values):
        def formatValue(value):
            return '0' if value == 0 else '{0:.3f}'.format(value)
        print '\t'.join([''] + xAxis)
        for y in yAxis:
            print '\t'.join([y] + [formatValue(values[y][x]) for x in xAxis ])

    printTable(states, states, transitionMatrix)
    print '------'
    printTable(alphabet, states, emissionMatrix)

    return states, transitionMatrix, emissionMatrix
#
if __name__ == '__main__':
#     alphabet, path, transitionMatrix = readPathProbabilityInputFile('data/pathprobability_challenge.txt')
#     print path
#     print transitionMatrix
#     print calcPathProbability(alphabet, path, transitionMatrix)

#    alphabet, path, hiddenPath, emissionMatrix = readEmissionProbabilityInputFile('data/emissionProbability_challenge.txt')
#    print calcEmissionPathProbability(alphabet, path, hiddenPath, emissionMatrix)

    #path, alphabet, states, transmissionMatrix, emissionMatrix = readViterbiInputFile('data/viterbi_sample.txt')
    
#     hiddenPath = viterbi(*readViterbiInputFile('data/viterbi_challenge.txt'))
#     print hiddenPath
    
#     probability = hmmProbability(*readViterbiInputFile('data/hmmProbability_challenge.txt'))
#     print probability

#    states, transitionMatrix, emissionMatrix = hmmProfile(*readHmmProfileFile('data/hmmProfile_sample.txt'))
    
#    states, transitionMatrix, emissionMatrix = hmmProfile(*readHmmProfileWithPseudoCountFile('data/hmmProfileWithPseudoCount_challenge.txt'))
    
    threshold, alphabet, alignments, pseudoCount, path = readHmmSequenceAlignmentFile('data/hmmSequenceAlignment_sample.txt')
    states, transitionMatrix, emissionMatrix = hmmProfile(threshold, alphabet, alignments, pseudoCount)
    hmm = viterbi(path, alphabet, states, transitionMatrix, emissionMatrix)
    print hmm
        