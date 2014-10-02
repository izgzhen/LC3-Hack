# Converter for LC-3 ISA
# Input: .bin or .hex
# Output: .obj

import sys
import binascii

fSource = open(sys.argv[1], 'r')
fDest = open(sys.argv[1][:-3] + 'obj', 'wb')

type = sys.argv[1][-3:]

content = ''.join(fSource.read().split())

if type == 'bin':
	content = hex(int(content, 2))[2:].zfill(len(content) / 4)[:-1]	

fDest.write(binascii.unhexlify(content))