# pylint: disable-msg=R0904
"""
Created on 25 Nov 2013

"""
import unittest
from stepic.assembly import stringComposition, overlapGraph, debruinGraph, debruinGraphFromKmers, \
     eulerianCycle, eulerianPath, stringReconstruction, pairedReads, contigs

class AssemblyTest(unittest.TestCase):

    def testStringComposition(self):
        with open('data/assembly/stringComposition.txt') as fp:
            with open('data/assembly/stringComposition.out', 'w') as scout:
                kmerLength = int(fp.readline())
                seq = fp.readline()
                for sc in stringComposition(seq, kmerLength):
                    scout.write(sc)
                    scout.write('\n')

    def testOverlapGraph(self):
        with open('data/assembly/overlapGraph.txt') as fp:
            for sc in overlapGraph([kmer.strip() for kmer in fp.readlines()]):
                print sc

    def testDeBruijn(self):
        with open('data/assembly/debruijnGraph.txt') as fp:
            with open('data/assembly/debruijnGraph.out', 'w') as scout:
                kmerLength = int(fp.readline())
                seq = fp.readline()
                for item in debruinGraph(seq, kmerLength):
                    print item
                    scout.write(item)
                    scout.write('\n')

    def testDeBruijnFromKmers(self):
        with open('data/assembly/debruijnGraphFromKmers.txt') as fp:
            with open('data/assembly/debruijnGraphFromKmers.out', 'w') as scout:
                kmers = [kmer.strip() for kmer in fp.readlines()]
                for item in debruinGraphFromKmers(kmers):
                    print item
                    scout.write(item)
                    scout.write('\n')

    def testEulerianCycle(self):
        with open('data/assembly/eulerianCycle.txt') as fp:
            nodes = { int(n[0]) : [int(x) for x in n[1].split(',')] for n in [l.strip().split(' -> ') for l in fp.readlines()]}
            print '->'.join([str(n) for n in eulerianCycle(nodes)])

    def testEulerianPath(self):
        with open('data/assembly/eulerianPath.txt') as fp:
            nodes = { int(n[0]) : [int(x) for x in n[1].split(',')] for n in [l.strip().split(' -> ') for l in fp.readlines()]}
            print '->'.join([str(n) for n in eulerianPath(nodes)])

    def testStringReconstruction(self):
        with open('data/assembly/stringReconstruction.txt') as fp:
            nodes = { n[0] : [x for x in n[1].split(',')] for n in [l.strip().split(' -> ') for l in fp.readlines()]}
            print stringReconstruction(nodes)

    def testPairedReads(self):
        with open('data/assembly/pairedReads.txt') as fp:
            dist = int(fp.readline())
            pairs = [l.strip().split('|') for l in fp.readlines()]
            print pairedReads(dist, pairs)

    def testConfig(self):
        with open('data/assembly/contigs.txt') as fp:
            kmers = [l.strip() for l in fp.readlines()]
            results = [c for c in contigs(kmers)]
            results.sort()
            print '\n'.join(results)
            print len(results)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
