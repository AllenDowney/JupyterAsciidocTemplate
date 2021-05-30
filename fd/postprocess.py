import re
import sys
import string

path = sys.argv[1]

with open(path) as fin:
    lines = fin.read().split('\n')

trans = str.maketrans('', '', string.punctuation)

for i in range(len(lines)):
    line = lines[i]
    if line.startswith('='):
        anchor = line.strip('=').replace(' ', '')
        anchor = anchor.translate(trans)
        lines[i] = f'[[_{anchor}]]\n' + line

with open(path, 'w') as fout:
    fout.write('\n'.join(lines))
