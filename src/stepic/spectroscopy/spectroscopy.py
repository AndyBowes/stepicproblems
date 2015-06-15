'''
Created on 11 Jun 2015

@author: Andy
'''
from constants import proteinMass
from itertools import chain
from re import match;
import networkx as nx


proteinLookup = {v:k for k,v in proteinMass.iteritems()}

def graph(spectrum):
    """
    """
    spectrum.append(0)
    spectrum.sort()
    for i in xrange(len(spectrum)-1):
        for j in xrange(i+1,len(spectrum)):
            mass = spectrum[j]-spectrum[i] 
            if mass in proteinLookup.keys():
                print '{0}->{1}:{2}'.format(spectrum[i],spectrum[j],proteinLookup[mass])
                
def idealSpectrum(peptide):
    """
    Generate the Ideal Spectrum for a supplied peptide.
    This includes all of the
    """
    def weight(peptideSeq):
        return sum(map(lambda x:proteinMass[x],peptideSeq))
    spectrum = []
    for i in xrange(1,len(peptide)+1):
        spectrum.append(weight(peptide[:i])) # Prefix
        spectrum.append(weight(peptide[i:])) # Suffix
    return sorted(spectrum)[1:] # Ignore the zero length suffix.
                
def decodeIdealSpectrum(spectrum):
    """
    Create a network of the links between nodes as a unidirectional graph and then 
    link the nodes which can be linked by appropriately weighted amino acids.
    """
    spectrum = [0] + sorted(spectrum)
    graph = nx.DiGraph()
    graph.add_nodes_from(xrange(len(spectrum)))
    
    for i in xrange(len(spectrum)-1):
        for j in xrange(i,len(spectrum)):
            mass = spectrum[j] - spectrum[i]
            if mass in proteinLookup.keys():
                graph.add_edge(i, j, {'amino': proteinLookup[mass]})

    for path in nx.all_simple_paths(graph, 0, len(spectrum)-1):
        peptide = ''.join(map(lambda x: graph[x[0]][x[1]]['amino'], zip(path[:-1],path[1:])))
        if idealSpectrum(peptide) == spectrum[1:]:
            return peptide
    return None

def toPeptideVector(peptide):
    """
    Convert a peptide to a vector which 
    """         
    return list(chain.from_iterable(['0'*(proteinMass[p]-1) + '1' for p in peptide ]))

def fromPeptideVector(vector):
    """
    Convert a peptide vector to a peptide
    """
    indexes = [-1] + [i for i, x in enumerate(vector.split(' ')) if x == '1']
    return ''.join(map(lambda x : proteinLookup[x], [indexes[i] - indexes[i-1] for i in xrange(1,len(indexes))]))

def peptideSequencing(spectralVector, proteins=None):
    
    if proteins is None:
        proteins = proteinMass
    graph = nx.DiGraph()
    maxIndex = len(spectralVector)
    graph.add_nodes_from(xrange(maxIndex))

    for idx in xrange(maxIndex):
        # Ignore nodes with no incoming edges except the 1st one.
        if idx > 0 and len(graph.in_edges(idx)) == 0:
            continue
        
        for p, mass in proteins.iteritems():
            if idx + mass < len(spectralVector):
                try:
                    graph.add_edge(idx, idx+mass,{'amino': p,
                                              'weight': -1 * spectralVector[idx+mass]})
                except IndexError as e:
                    pass
    
    pred, dist = nx.bellman_ford(graph, 0)
    proteinLookup = {v:k for k,v in proteins.iteritems()}    
    idx = len(spectralVector)-1
    path = []
    while idx > 0:
        path.append(proteinLookup[idx-pred[idx]])
        idx = pred[idx]
    return ''.join(path[::-1])

def scorePeptideVector(vector, spectrum):
    """
    """
    return sum(map(lambda x: x[0]*x[1],zip(map(int,vector), spectrum)))

def peptideIdentification(spectrum, proteome):
    maxScore = 0
    bestProtein = None
    for i in xrange(len(proteome)-1):
        for j in xrange(i, len(proteome)):
            peptide = proteome[i:j+1]
            vector = toPeptideVector(peptide)
            if len(vector) > len(spectrum):
                break
            if len(vector) == len(spectrum):
                score = scorePeptideVector(vector, spectrum)
                if score > maxScore:
                    maxScore = score
                    bestProtein = peptide
    return bestProtein, maxScore
            
def psmSearch(spectrums,proteome,threshold):
    for spectrum in spectrums:
        peptide, score = peptideIdentification(spectrum, proteome)
        if score >= threshold:
            yield peptide
    

if __name__ == '__main__':
    #print idealSpectrum('GPAG')
#    print ' '.join(toPeptideVector('AHLTFKGEGRIAPENQFTFCQDLEWWSHCSQYL'))
#    with open('data/fromPeptideVector_extra.txt') as fp:
#        print fromPeptideVector(fp.readline().strip())
#    with open('data/decodeIdealSpectrum_challenge.txt') as fp:
#        print decodeIdealSpectrum(map(int, fp.readline().strip().split(' ')))
#     with open('data/peptideSequencing_challenge.txt') as fp:
#         print peptideSequencing(map(int, fp.readline().strip().split(' ')))
        
#     with open('data/peptideIdentification_challenge.txt') as fp:
#         spectrum = map(int, fp.readline().strip().split(' '))
#         proteome = fp.readline().strip()
#         print peptideIdentification(spectrum[1:], proteome)
        
    with open('data/psmSearch_challenge.txt') as fp:
        line = fp.readline()
        spectrums = []
        while match('^[0-9\-].*', line):
            spectrums.append( map(int, line.strip().split(' '))[1:])
            line = fp.readline()
        proteome = line.strip()
        threshold = int(fp.readline().strip())
        print '\n'.join(psmSearch(spectrums, proteome, threshold))
        
                