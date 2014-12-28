from defs import *
import re
from tokens import *

def SEX(integer, length):
	if integer >= 0:
		binary = bin(integer)[2:]
		if len(binary) > length:
			return binary[:length]
		elif len(binary) < length:
			return '0' * (length - len(binary)) + binary
		else:
			return binary
	else:
		return transform(ZEX(- integer, length))


def transform(original):
	# Get complement and plus one
	notTable = {'0' : '1', '1' : '0'}
	length = len(original)
	flag = False
	new = map(lambda x : x, ''.zfill(length))

	for i in range(length):
		back = length - 1 - i
		origBit = original[back]

		new[back] = notTable[origBit] if flag else origBit
		if (not flag) and origBit == '1':
			flag = True
			continue

	return ''.join(new)[:length]

def ZEX(integer, length):
	binary = bin(integer)[2:]
	if len(binary) > length:
		return binary[:length]
	elif len(binary) < length:
		return '0' * (length - len(binary)) + binary
	else:
		return binary

def isOpcode(op):
	if re.match(t_OP_BR, op):
		return True
	else:
		return op in opcode or op in popcode or op in trap_vectors

def toInt(string):
	if re.match(r'[xX][0-9a-fA-F]+', string):
		return int(string[1:], 16)
	elif re.match(r'[#][0-9]+', string):
		return int(string[1:])