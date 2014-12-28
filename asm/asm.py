tokens = (
	'OP_ADD',
	'REG',
	)

def t_REG(t):
	r'[rR][0-7]'
	t.value = bin(int(t.value[1]))[2:].zfill(3)
	return t

t_OP_ADD = r'ADD'
t_ignore = ' ,\t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

import ply.lex as lex
lexer = lex.lex()

opcode = {
	'ADD' : '0001'
}

def p_OP_ADD(t):
	'''inst : OP_ADD operands'''
	t[0] = opcode['ADD'] + t[2]
	print(t[0])

def p_OPERANDS(t):
	'''operands : REG REG REG'''
	t[0] = t[1] + t[2] + '000' + t[3]

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
yacc.yacc()

s = ('ADD R1, R2, R3')
yacc.parse(s)

# while 1:
# 	s = raw_input('inst > ')
# 	yacc.parse(s)