#!/usr/bin/env python
import sys
from struct import pack
from VariableBiteCode import vb_encode

if len(sys.argv) < 2:
    print "usage: %s in.txt > out.txt" % sys.argv[0]
    sys.exit(1)

for line in open(sys.argv[1], 'r'):
    (tag, id_list) = line.rstrip().split('\t')
    bytes = []
    pre = 0
    for id in id_list.split(','):
        id = int(id)
        bytes.append(vb_encode(id - pre))
        pre = id
    data = ''.join(bytes)
    sys.stdout.write('%s%s%s' % (
        pack('=2i', len(tag), len(data)), tag, data))

