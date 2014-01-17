"""
Created on 14 Jan 2014

"""

def burrowWheelerTransform(sequence):
    """
    Perform Burrow Wheeler Transform
    """
    array = [i for i in range(len(sequence))]
    array.sort(lambda x, y: cmp(sequence[x:x + 10000], sequence[y:y + 10000]))
    return ''.join([sequence[x - 1] for x in array])

def inverseBurrowWheelerTransform(sequence):
    """
    Reverse the Burrow Wheeler Transform
    """
    mapping = sorted([(i, v) for i, v in enumerate(sequence)], key=lambda x: x[1])
    first = [m[1] for m in mapping]
    firstLast = [m[0] for m in mapping]
    def process():
        pos = 0
        while firstLast[pos] != 0:
            pos = firstLast[pos]
            yield first[pos]
        yield '$'
    return ''.join(process())

def firstLast(bwt):
    mapping = sorted([(i, v) for i, v in enumerate(bwt)], key=lambda x: x[1])
    first = ''.join([m[1] for m in mapping])
    lastToFirst = [m[0] for m in mapping]
    print mapping
    return first, lastToFirst

def findPatterns(bwt, patterns):
    """
    Find number of matches of multiple Patterns in the sequence
    """
    first, lastToFirst = firstLast(bwt)
    for pattern in patterns:
        yield bwmatching(first, bwt, pattern, lastToFirst)

def bwmatching(firstColumn, lastColumn, pattern, lastToFirst):
    top = 0
    bottom = len(lastColumn)
    while top <= bottom:
        if pattern:
            symbol = pattern[-1]
            pattern = pattern[:-1]
            if symbol in lastColumn[top:bottom + 1]:
                symbolIndexes = find(lastColumn[top:bottom + 1], symbol, top)
                indexValues = [lastToFirst[i] for i in symbolIndexes]
                print symbolIndexes
                print indexValues
                topIndex = min(indexValues)
                bottomIndex = max(indexValues)
                top = lastToFirst[topIndex]
                bottom = lastToFirst[bottomIndex]
                print topIndex, bottomIndex, lastColumn[topIndex], lastColumn[bottomIndex], top, bottom
            else:
                return 0
    return (bottom - top) + 1

def find(s, ch, offset):
    return [offset + i for i, ltr in enumerate(s) if ltr == ch]

if __name__ == '__main__':  # pragma: no cover
#    print burrowWheelerTransform('GCGTGCCTGGTCA$')
#    print inverseBurrowWheelerTransform('enwvpeoseu$llt')
    for o in findPatterns('TCCTCTATGAGATCCTATTCTATGAAACCTTCA$GACCAAAATTCTCCGGC', ['CCT', 'CAC', 'GAG', 'CAG', 'ATC']):
        print o
