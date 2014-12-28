from defs import *
import re

t_OP_ADD = 'ADD'
t_OP_AND = 'AND'
t_OP_JMP = 'JMP'
t_OP_LDR = 'LDR'
t_OP_TRAP = 'TRAP'
t_OP_ST = 'ST'
t_OP_STI = 'STI'
t_OP_STR = 'STR'
t_OP_NOT = 'NOT'
t_OP_RET = 'RET'
t_OP_JSR = 'JSR'
t_OP_JSRR = 'JSRR'
t_OP_LD = 'LD'
t_OP_LDI = 'LDI'
t_OP_LEA = 'LEA'
t_OP_RTI = 'RTI'
t_POP_FILL = '.FILL'

t_OP_BR  = r'BRn?z?p?'
t_ignore = ' ,\t'

def t_REG(t):
	r'[rR][0-7]'
	t.value = bin(int(t.value[1]))[2:].zfill(3)
	return t	

def t_HEX(t):
	r'[xX][0-9a-fA-F]+'
	t.value = int(t.value[1:], 16)
	return t

def t_N_HEX(t):
	r'[xX]-[0-9a-fA-F]+'
	t.value = -int(t.value[2:], 16)
	return t

def t_DECIMAL(t):
	r'[#][0-9]+'
	t.value = int(t.value[1:])
	return t

def t_N_DECIMAL(t):
	r'[#]-[0-9]+'
	t.value = -int(t.value[2:])
	return t

def t_error(t):
	print("Illegal character '%s'" % t.value)
	t.lexer.skip(1)