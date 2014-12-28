from defs import *
import re
from tokens import *

def SEX(integer, length):
	if integer >= 0:
		binary = bin(integer)[2:]
	else:
		binary = bin(integer)[3:]

	ex_bit = '0' if integer > 0 else '1'

	if len(binary) > length:
		return binary[:length]
	elif len(binary) < length:
		return ex_bit * (length - len(binary)) + binary
	else:
		return binary

def ZEX(integer, length):
	binary = bin(integer)[2:]
	if len(binary) > length:
		return binary[:length]
	elif len(binary) < length:
		return '0' * (length - len(binary)) + binary
	else:
		return binary

def isOpcode(op):
	return op in opcode or op in popcode or op in trap_vectors