'''
Created on 24 Oct 2013

@author: root
'''
from string import maketrans

DNA_BASES = ['A','C','G','T']

def reverseComplement(dna):
    return dna.translate(maketrans('ACGT','TGCA'))[::-1]