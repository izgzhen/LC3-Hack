import binascii
import sys

f = open(sys.argv[1], 'rb');

content = f.read()

content = binascii.hexlify(content)

content = bin(int(content,16))[2:].zfill(len(content) * 4)

length = len(content) / 16

print length

for i in range(length):
 	print content[i*16:(i+1)*16]