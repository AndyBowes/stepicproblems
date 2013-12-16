"""
Created on 14 Dec 2013

"""
# pylint:disable=W0621, C0103, C0111
def readMatrix(fp):
    matrix = {}
    headers = fp.readline().split()
    for row in fp.readlines():
        elements = row.split()
        matrix[elements[0]] = {headers[index]:int(value) for index, value in enumerate(elements[1:])}
    return matrix

if __name__ == '__main__':
    with open('data/PAM250Matrix.txt') as fp:
        print readMatrix(fp)
