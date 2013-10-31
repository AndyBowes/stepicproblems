'''
Created on 24 Oct 2013

@author: Andy Bowes
'''

from itertools import takewhile,product
from re import findall
from collections import defaultdict
from dna import reverseComplement
from copy import copy

aminoAcids = {'A': 71, 'C': 103, 'E': 129, 'D': 115, 'G': 57, 'F': 147, 'I': 113, 'H': 137,
              'K': 128, 'M': 131, 'L': 113, 'N': 114, 'Q': 128, 'P': 97, 'S': 87, 'R': 156,
              'T': 101, 'W': 186, 'V': 99, 'Y': 163}

rnaCoding = {'ACC': 'T', 'GCA': 'A', 'AAG': 'K', 'AAA': 'K', 'GUU': 'V', 'AAC': 'N', 'AGG': 'R', 'UGG': 'W', 'GUC': 'V',
             'AGC': 'S', 'ACA': 'T', 'AGA': 'R', 'AAU': 'N', 'ACU': 'T', 'GUG': 'V', 'CAC': 'H', 'ACG': 'T', 'AGU': 'S',
             'CCA': 'P', 'CAA': 'Q', 'CCC': 'P', 'UGU': 'C', 'GGU': 'G', 'UCU': 'S', 'GCG': 'A', 'CGA': 'R', 'CAG': 'Q',
             'CGC': 'R', 'UAU': 'Y', 'CGG': 'R', 'UCG': 'S', 'CCU': 'P', 'GGG': 'G', 'GGA': 'G', 'GGC': 'G', 'CCG': 'P',
             'UCC': 'S', 'UAC': 'Y', 'CGU': 'R', 'GAA': 'E', 'AUA': 'I', 'AUC': 'I', 'CUU': 'L', 'UCA': 'S', 'AUG': 'M',
             'UGA': 'STOP', 'CUG': 'L', 'GAG': 'E', 'AUU': 'I', 'CAU': 'H', 'CUA': 'L', 'UAA': 'STOP', 'GCC': 'A',
             'UUU': 'F', 'GAC': 'D', 'GUA': 'V', 'UGC': 'C', 'GCU': 'A', 'UAG': 'STOP', 'CUC': 'L', 'UUG': 'L', 'UUA': 'L', 'GAU': 'D', 'UUC': 'F'}

def readCodingTable():
    with open('rna_coding.txt') as fp:
        lines = [l.strip().split(' ') for l in fp.readlines()]
        rna_codes = { l[0]:l[1] for l in lines }
        print rna_codes

def readAminoAcids():
    with open('aminoAcid.txt') as fp:
        lines = [l.strip().split(' ') for l in fp.readlines()]
        aminos = { l[0]:int(l[1]) for l in lines }
        print aminos


def proteinTranslation(rna):
    """
    Translate RNA into a Protein
    """
    protein = [rnaCoding[codon] for codon in takewhile( lambda codon: rnaCoding[codon] != 'STOP', findall(r'...', rna)) ]
    return "".join(protein)

def peptideEncoding(dna,protein):
    """
    Find motifs in the positions dna which generate the protein
    """
    reverseLookup = defaultdict(list)
    for k,v in rnaCoding.iteritems():reverseLookup[v].append(k.replace('U', 'T'))
    motifs = [ "".join(prod) for prod in product(*[reverseLookup[p] for p in protein])]
    motifs += [reverseComplement(m) for m in motifs]
    motifLength = 3*len(protein)
    return [dna[i:i+motifLength] for i in range(len(dna)-motifLength) if dna[i:i+motifLength] in motifs]
  
def cyclicsubpeptides(protein):
    doubleProtein = protein*2
    return [doubleProtein[i:i+j] for i in range(len(protein)) for j in range(1,len(protein)) ]

def cyclicSpectrum(protein):
    peptides = cyclicsubpeptides(protein) + ['',protein]
    spectrum = [sum([aminoAcids[a] for a in p]) for p in peptides]
    return sorted( spectrum) 

def subpeptides(protein):
    return [protein[i:i+j] for i in range(len(protein)) for j in range(1,len(protein)-i) ]

def linearSpectrum(protein):
    peptides = subpeptides(protein) + ['',protein]
    spectrum = [sum([aminoAcids[a] for a in p]) for p in peptides]
    return sorted( spectrum) 

def cyclopeptideSequencing(spectrum):
    p = dict(zip(aminoAcids.values(),aminoAcids.keys()))
    available = [p[s] for s in spectrum if s in aminoAcids.itervalues()]
    peptides = available
    while len(peptides) > 0:
        peptides = list(set(["".join(p) for p in product(peptides,available)]))
        print 'Before:' + ",".join(peptides)
        for peptide in copy(peptides):
            peptideSpectrum = linearSpectrum(peptide)
            if cyclicSpectrum(peptide) == spectrum:
                yield peptideToMassChain(peptide)
                peptides.remove(peptide)
            elif not sublist(peptideSpectrum, spectrum):
                peptides.remove(peptide)
        print 'After:' + ",".join(peptides)
        
def peptideWeight(peptide):
    return sum([aminoAcids[a] for a in peptide])
                
def leaderboardCyclopeptideSequencing(spectrum, n):
    
    def cut(leaderboard,n):
        leaders = []
        scores = sorted(leaderboard.iterkeys(),key=lambda x: x,reverse=True)
        for s in takewhile(lambda _: len(leaders)<n,scores):
            leaders.extend(leaderboard[s])
        return leaders
        
    p = dict(zip(aminoAcids.values(),aminoAcids.keys()))
    available = list(p.itervalues())
    peptides = available
    bestScore = 0
    bestPeptide = None
    while len(peptides) > 0:
        leaderboard = defaultdict(list)
        peptides = ["".join(p) for p in product(peptides,available)]
#        print 'Before:' + ",".join(peptides)
        for peptide in copy(peptides):
            weight = peptideWeight(peptide)
            if weight > spectrum[-1]:
                peptides.remove(peptide)
            else:
                peptideSpectrum = cyclicSpectrum(peptide)
                peptideScore = score(peptideSpectrum, spectrum)
                if weight == spectrum[-1]:
#                    peptideScore = score(cyclicSpectrum(peptide), spectrum)
                    if peptideScore > bestScore:
                        bestPeptide = peptide
                        bestScore = peptideScore
                leaderboard[peptideScore].append(peptide)
        # Take the highest N scores from the round
        peptides = cut(leaderboard,n)
#        print 'After:' + ",".join(peptides)
    print bestScore
    print cyclicSpectrum(bestPeptide)
    return peptideToMassChain(bestPeptide)        

def peptideToMassChain(peptide):
    return '-'.join(str(aminoAcids[a]) for a in peptide)

def score(list1,list2):
    occurs2 = occurs(list2)
    occurs1 = occurs(list1)
    return sum([min(occurs1[k],occurs2[k]) for k,_ in occurs1.iteritems()])

def occurs(inList):
    occurs = defaultdict(int)
    for i in inList: occurs[i] += 1
    return occurs

def sublist(list1, list2):
    occurs2 = occurs(list2)
    return all([v <= occurs2[k] for k, v in occurs(list1).iteritems()])

if __name__ == "__main__":
#    print ' '.join(sorted(["-".join(str(aminoAcids[x]) for x in pep) for pep in cyclopeptideSequencing([0,113,128,186,241,299,314,427])]))
    print leaderboardCyclopeptideSequencing([0,71,113,129,147,200,218,260,313,331,347,389,460],20)