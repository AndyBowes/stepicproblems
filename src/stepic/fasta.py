'''
Created on 4 May 2013

@author: Andy

Read FASTA Format files
'''
def read_fasta(fp):
    name, seq = None, []
    for line in fp:
        line = line.rstrip()
        if line.startswith(">"):
            if name: yield (name, ''.join(seq))
            name, seq = line[1:], []
        else:
            seq.append(line)
    if name: yield (name, ''.join(seq))

#with open('f.fasta') as fp:
#    for name, seq in read_fasta(fp):
#       print(name, seq)