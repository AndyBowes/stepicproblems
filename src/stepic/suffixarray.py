"""
Created on 13 Jan 2014

"""

def buildSuffixArray(sequence):
    array = [i for i in range(len(sequence))]
    array.sort(lambda x, y: cmp(sequence[x:], sequence[y:]))
    return array

if __name__ == '__main__':  # pragma: no cover
    print ', '.join([str(x) for x in buildSuffixArray('AACGATAGCGGTAGA$')])
