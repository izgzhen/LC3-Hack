tokens = (
	'OP_ADD',
	'OP_AND',
	'OP_BR',
	'REG',
	'HEX',
	'DECIMAL',
	'N_HEX',
	'N_DECIMAL',
	'P_OP',
	)

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
	r'[#]?[0-9]+'
	t.value = int(t.value[1:])
	return t

def t_N_DECIMAL(t):
	r'[#]?-[0-9]+'
	t.value = -int(t.value[2:])
	return t


def SEX(integer, length):
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

t_OP_ADD = 'ADD'
t_OP_AND = 'AND'
t_OP_BR = r'BRn?z?p?'
t_ignore = ' ,\t'
t_P_OP   = r'\.[A-Za-z][A-Za-z_0-9]+'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

import ply.lex as lex
lexer = lex.lex()

symbols = {}

opcode = {
	'ADD' : '0001',
	'AND' : '0101',
	'BR'  : '0000'
}



popcode = {}

def isOpcode(op):
	if op in opcode or op in popcode:
		return True

	if re.match(t_OP_BR, op):
		return True

	return False

def p_P_OP_inst(t):
	'''inst : P_OP HEX'''
	t[0] = ZEX(t[2], 16)

def p_OP_ADD(t):
	'''inst : OP_ADD RRR
			| OP_ADD RRI'''
	t[0] = opcode['ADD'] + t[2]

def p_OP_AND(t):
	'''inst : OP_AND RRR
			| OP_AND RRI'''
	t[0] = opcode['AND'] + t[2]

def p_OP_BR(t):
	'''inst : OP_BR OFFSET9'''
	nzp = ['1','1','1']
	nzp[0] = '1' if 'n' in t[1] else '0'
	nzp[1] = '1' if 'z' in t[1] else '0'
	nzp[2] = '1' if 'p' in t[1] else '0'

	t[0] = opcode['BR'] + ''.join(nzp) + t[2]

def p_VALUE(t):
	'''VALUE : HEX
			 | DECIMAL
			 | N_DECIMAL
			 | N_HEX'''
	t[0] = t[1]

def p_OFFSET9(t):
	'''OFFSET9 : VALUE'''
	# print t[1]
 	t[0] = SEX(t[1], 9)

def p_IMM5(t):
	'''IMM5 : VALUE'''
	t[0] = ZEX(t[1], 5)

def p_RRR(t):
	'''RRR : REG REG REG'''
	t[0] = t[1] + t[2] + '000' + t[3]

def p_RRI(t):
	'''RRI : REG REG IMM5'''
	t[0] = t[1] + t[2] + '1' + t[3]

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
yacc.yacc()

f = open("test.asm", 'r')

lines = f.read().split('\n')

import re

# .ORIG Check
assert(not (lines[0].split()[0] == '.ORIG' and re.match(r'[xX][-]?[0-9a-fA-F]+', lines[0].split()[1]) and len(lines) == 2))

line_counter = int(lines[0].split()[1][1:], 16)

assert(line_counter >= 0 and line_counter < 65535)

for line in lines[1:]:
	pre_split = line.split()
	if pre_split[0] == '.END':
		break

	if isOpcode(pre_split[0]):
		print yacc.parse(line)
	else:
		symbols[pre_split[0]] = line_counter
		print yacc.parse(''.join(pre_split[1:]))
	line_counter = line_counter + 1

# .END Check
assert(lines[-1].split()[0] == '.END' and len(lines[-1].split()) == 1)

print "\n=== symbol table ==="
for symbol in symbols:
	print symbol, ':', hex(symbols[symbol])