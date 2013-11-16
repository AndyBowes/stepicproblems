'''
Created on 15 Oct 2013

@author: Andy
'''
def skew(dna):
    x = 0
    yield x
    for base in dna:
        if base == 'C': x -= 1
        if base == 'G': x += 1
        yield x
        
def skewMinPosition(dna):
    skews = list(skew(dna))
    low = min(skews)
    return [i for i, j in enumerate(skews) if j == low]
