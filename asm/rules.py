from tools import *
from defs import *

def p_POP_FILL(t):
	'''inst : POP_FILL VALUE'''
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
	'''inst : OP_BR VALUE '''
	nzp = ['1','1','1']
	nzp[0] = '1' if 'n' in t[1] else '0'
	nzp[1] = '1' if 'z' in t[1] else '0'
	nzp[2] = '1' if 'p' in t[1] else '0'

	t[0] = opcode['BR'] + ''.join(nzp) + SEX(t[2], 9)

def p_OP_JMP(t):
	'''inst : OP_JMP REG'''
	t[0] = opcode['JMP'] + '000' + t[2] + '000000'

def p_OP_LDR(t):
	'''inst : OP_LDR REG REG VALUE'''
	t[0] = opcode['LDR'] + t[2] + t[3] + SEX(t[4], 6)

def p_OP_TRAP(t):
	'''inst : OP_TRAP VALUE'''
	t[0] = opcode['LDR'] + '0000' + ZEX(t[2], 8)

def p_OP_NOT(t):
	'''inst : OP_NOT REG REG'''
	t[0] = opcode['NOT'] + t[2] + t[3] + '111111'

def p_OP_RET(t):
	'''inst : OP_RET'''
	t[0] = opcode['RET'] + '000111000000'

def p_OP_JSR(t):
	'''inst : OP_JSR VALUE'''
	t[0] = opcode['JSR'] + '1' + SEX(t[2], 11)

def p_OP_JSRR(t):
	'''inst : OP_JSRR REG'''
	t[0] = opcode['JSRR'] + '000' + t[2] + '000000'

def p_OP_LDx(t):
	'''inst : OP_LD REG VALUE
			| OP_LDI REG VALUE
			| OP_LEA REG VALUE'''
	t[0] = opcode[t[1]] + t[2] + SEX(t[3], 9)

def p_OP_RTI(t):
	'''inst : OP_RTI'''
	t[0] = opcode['RTI'] + '000000000000'



def p_VALUE(t):
	'''VALUE : HEX
			 | DECIMAL
			 | N_DECIMAL
			 | N_HEX'''
	t[0] = t[1]

def p_RRR(t):
	'''RRR : REG REG REG'''
	t[0] = t[1] + t[2] + '000' + t[3]

def p_RRI(t):
	'''RRI : REG REG VALUE'''
	t[0] = t[1] + t[2] + '1' + ZEX(t[3], 5)

def p_error(t):
    print("Syntax error at '%s'" % t.value)