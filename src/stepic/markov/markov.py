'''
Created on 21 May 2015

@author: Andy Bowes
'''
from math import log
from itertools import product, chain, groupby
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

def viterbi2(path, alphabet, states, transitionMatrix, emissionMatrix, noOfSeedColumns):
    """
    
    """
    directions = {'M':(-1,-1),'D':(-1,0),'I':(0,-1)}
    
    graph = [[ None for _ in xrange(len(path)+1)] for _ in xrange(noOfSeedColumns + 1)]
    graph[0][0] = {'S' : ('S', 1.0)}
    
    def getStates(i, j, direction):
        iHash = i + direction[1][0]
        jHash = j + direction[1][1]
        return [ ('{0}{1}'.format(direction[0],i), fromState, prob[1]) for fromState, prob in graph[iHash][jHash].iteritems()]

    def emissionProb(toState, emittedChar):
        return 1.0 if toState[0] == 'D' else emissionMatrix[toState][emittedChar]
    
    def transitionProb(fromState, toState):
        return transitionMatrix[fromState][toState]
    
    def weight(fromState, toState, emittedChar):
        return transitionProb(fromState, toState) * emissionProb(toState, emittedChar)
    
    graph[0][1] = { 'I0' : ('S', graph[0][0]['S'][1] * weight('S','I0',path[0]))}
    for j in xrange(2,len(path)+1):
        graph[0][j] = { 'I0' : ('I0', graph[0][j-1]['I0'][1] * weight('I0','I0',path[j-1]))}
    
    for i in xrange(1,noOfSeedColumns+1):
        fromState, toState = 'D' + str(i-1) if i > 1 else 'S', 'D' + str(i)
        graph[i][0] = {toState : (fromState, graph[i-1][0][fromState][1] * transitionMatrix[fromState][toState])}
    
    for (i,j) in product(xrange(1, noOfSeedColumns+1), xrange(1, len(path)+1)):
        emittedChar = path[j-1]
        probs = sorted(chain.from_iterable([[(toState, fromState, prob * weight(fromState, toState, emittedChar)) for toState, fromState, prob in getStates(i,j,direction)]      
                     for direction in directions.iteritems()]),key=lambda t: t[0])
        elementValue = {k:max([i[1:]  for i in list(group)], key=lambda x:x[1]) for k, group in groupby(probs, lambda x: x[0])}
        
        graph[i][j] = elementValue

    # Start at the last cell and work backwards until you reach 0, 0
    i = noOfSeedColumns
    j = len(path)
    
    
    finalSteps = [(k, element[1] * transitionProb(k,'E')) for k, element in graph[i][j].iteritems()]
#     print finalSteps
    step, _ = max(finalSteps, key=lambda x : x[1])
    
    hmm = []
    try:
        while (i+j) > 0:
            hmm.append(step)
            nextStep = graph[i][j][step][0]
            i += directions[step[0]][0]
            j += directions[step[0]][1]
            step = nextStep
    except KeyError as e:
        print 'Error'
        print i,j, step
        print graph[i][j]
        raise e
    return hmm[::-1] # Reverse the HMM
    

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

def readHmmSoftDecodingFile(filePath):
    """
    Read information for the Soft Decoding Problem.
    
    Determines the probability of each state of the HMM at each position.
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
    

def hmmSoftDecoding(path, alphabet, states, transitionMatrix, emissionMatrix):
    """
    
    """
    def characterScore(fromState, toState, emittedChar, previousScores):
        try:
            return previousScores[fromState] * transitionMatrix[fromState][toState] * emissionMatrix[toState][emittedChar]
        except TypeError as e:
            raise e
        
    graph = [{ state : 1.0/len(states) * emissionMatrix[state][path[0]] for state in states}]
    
    # Go through the path
    for n in xrange(1,len(path)):
        emittedChar = path[n]
        previousScores = graph[-1]
        newScores = {toState : sum(map(lambda fromState: characterScore(fromState, toState, emittedChar, previousScores), states )) for toState in states }
        graph.append(newScores)

    forwardGraph = graph
    forwardTotal = sum(graph[-1].itervalues())
    
    path = path[::-1] # Reverse the path
    # Need to reverse the Transition Matrix
    graph = [{ state : 1.0 for state in states}]

#     reversedTransitionMatrix = {state : {} for state in states}
#     for state1, state2 in product(states,states):
#         reversedTransitionMatrix[state1][state2] = transitionMatrix[state2][state1]
# 
#     transitionMatrix = reversedTransitionMatrix

    def reverseCharacterScore(fromState, toState, emittedChar, previousScores):
        try:
            return previousScores[fromState] * transitionMatrix[toState][fromState] * emissionMatrix[fromState][emittedChar]
        except TypeError as e:
            raise e

    # Go through the reversed path
    for n in xrange(0,len(path)-1):
        emittedChar = path[n]
        previousScores = graph[-1]
        newScores = {toState : sum(map(lambda fromState: reverseCharacterScore(fromState, toState, emittedChar, previousScores), states )) for toState in states }
        graph.append(newScores)

    return map( lambda f : { state: (f[0][state] * f[1][state])/forwardTotal for state in states}, zip(forwardGraph, graph[::-1]))


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

    # Apply the Pseudocount adjustment if required
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

    return states, transitionMatrix, emissionMatrix, noOfSeedColumns

    
def printTable(xAxis,yAxis,values):
    def formatValue(value):
        return '0' if value == 0 else '{0:.3f}'.format(value)
    print '\t'.join([''] + xAxis)
    for y in yAxis:
        print '\t'.join([y] + [formatValue(values[y][x]) for x in xAxis ])

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
#    printTable(states, states, transitionMatrix)
#    print '------'
#    printTable(alphabet, states, emissionMatrix)
    
#     threshold, alphabet, alignments, pseudoCount, path = readHmmSequenceAlignmentFile('data/hmmSequenceAlignment_challenge.txt')
#     states, transitionMatrix, emissionMatrix, noOfSeedColumns = hmmProfile(threshold, alphabet, alignments, pseudoCount)
# 
#     hmm = viterbi2(path, alphabet, states, transitionMatrix, emissionMatrix, noOfSeedColumns)
#     print ' '.join(hmm)

    path, alphabet, states, transmissionMatrix, emissionMatrix = readHmmSoftDecodingFile('data/hmmSoftDecoding_challenge.txt')
    probabilities = hmmSoftDecoding(path, alphabet, states, transmissionMatrix, emissionMatrix)
    print '\t'.join(states)
    for p in probabilities:
        print '\t'.join([ '{0:.4f}'.format(p[state]) for state in states])


        