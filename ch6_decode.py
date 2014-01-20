#!/usr/bin/env python
import sys
from struct import unpack
from VariableBiteCode import vb_decode
 
if len(sys.argv) < 2:
    print "usage: %s in.txt > out.txt" % sys.argv[0]
    sys.exit(1)

fp = open(sys.argv[1], 'rb')
while True:
    bytes = fp.read(8)
    if not bytes:
        break
    (tag_len, id_list_len) = unpack('=2i', bytes)
    tag = fp.read(tag_len)
    id_list = []
    pre = 0
    r = fp.read(id_list_len)
    for id in vb_decode(r):
        id_list.append('%s' % (id + pre))
        pre = id + pre
    sys.stdout.write('%s\t%s\n' % (tag, ','.join(id_list)))

fp.close()

