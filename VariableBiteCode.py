#!/usr/bin/env python
from struct import pack, unpack

# http://nlp.stanford.edu/IR-book/html/htmledition/variable-byte-codes-1.html
def vb_encode(numbers):
    if isinstance(numbers, int):
        return vb_encode_number(numbers)

    bytestream = ''
    for n in numbers:
        bytes = vb_encode_number(n)
        bytestream += bytes
    return bytestream

def vb_encode_number_orginal(n):
    bytes = []
    bytestream = ''
    while True:
        bytes.insert(0, n%128)
        if n < 128:
            break
        n = n / 128
    bytes[-1] += 128
    for byte in bytes:
        bytestream += pack('B', byte)
    return bytestream

# http://websystemsengineering.blogspot.jp/2012/12/variable-byte-code-how-to.html
def vb_encode_number(n):
    i = 0
    bytestream = ''
    while True:
        if i == 0:
            bytestream += pack('B', (n & 0b1111111) + 128)
        else:
            bytestream = pack('B', (n & 0b1111111)) + bytestream
        if n < 128:
            break
        n = n >> 7
        i += 1
    return bytestream

def vb_decode(bytestream):
    numbers = []
    n = 0
    unpacked = unpack('%dB' % len(bytestream), bytestream)
    for i in range(len(unpacked)):
        if unpacked[i] < 128:
            n = 128 * n + unpacked[i]
        else:
            n = 128 * n + (unpacked[i] - 128)
            numbers.append(n)
            n = 0
    return numbers

# http://www.ninxit.com/blog/2010/12/15/vbcode-python/
def vb_encode_X(numbers):
    if isinstance(numbers, int):
        numbers = [numbers]
    bytestream = ''
    for n in numbers:
        bytes = []
        while True:
            bytes.insert(0, n % 128)
            if n < 128:
                break
            n = n / 128
        bytes[-1] += 128
        bytestream += pack('%dB' % len(bytes), *bytes)
    return bytestream

def vb_decode_X(bytestream):
    n = 0
    numbers = []
    bytestream = unpack('%dB' % len(bytestream), bytestream)
    for byte in bytestream:
        if byte < 128:
            n = 128 * n + byte
        else:
            n = 128 * n + (byte - 128)
            numbers.append(n)
            n = 0
    return numbers


def get_bit(byteval,idx):
    return ((byteval&(1<<idx))!=0);


# test
if __name__ == '__main__':
    # format() require python 2.6 or more.

    bytestream = vb_encode([17,0,0])
    print ''.join([format(b, '08b') for b in unpack('%dB' % len(bytestream), bytestream)])
    print vb_decode(bytestream)

    def test_vb_encode(numbers, ok):
        bytestream = vb_encode(numbers)
        assert ''.join([format(b, '08b') for b in unpack('%dB' % len(bytestream), bytestream)]) == ok
        print "test ok. %s -> %s" % (numbers, ok)
    
    test_vb_encode(1,   '10000001')
    test_vb_encode(5,   '10000101')
    test_vb_encode(127, '11111111')
    test_vb_encode(128, '00000001' + '10000000')
    test_vb_encode(129, '00000001' + '10000001')
    test_vb_encode(210192, '00001100'+'01101010'+'10010000')

    import sys, random
    for i in xrange(1000):
        n = random.randint(0, sys.maxint)
        assert vb_decode(vb_encode(n))[0] == n

