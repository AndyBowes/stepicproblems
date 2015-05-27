'''
Created on 21 May 2015

@author: Andy
'''
from math import log
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
    
    probability = hmmProbability(*readViterbiInputFile('data/hmmProbability_challenge.txt'))
    print probability
    
        