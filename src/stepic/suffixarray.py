"""
Created on 13 Jan 2014

"""

def buildSuffixArray(sequence):
    array = [(i, sequence[i:]) for i in range(len(sequence))]
    array.sort(key=lambda x : x[1])
    return array

if __name__ == '__main__':  # pragma: no cover
    print ', '.join([str(x) for x, _ in buildSuffixArray('AACGATAGCGGTAGA$')])
