'''
Created on 18 Oct 2013

@author: Andy
'''
from itertools import product, ifilter

def probability(length,alphabet,pattern,minOccurs=1):
    words = list([ "".join(p) for p in product(alphabet,repeat=length)])
    print len(words)
    matches = [match for match in ifilter(lambda x: x.count(pattern) >= minOccurs, words)]
    matchCount = float(len(matches))
    print len(words) - matchCount
    print str(matchCount / len(words))

def probCount(length=25,alphabet=['0','1']):
    print len(list(product(alphabet,repeat=length)))