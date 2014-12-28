from tokens import *
from tools import *
from rules import *

import ply.lex as lex
import ply.yacc as yacc

symbols = {} # Symbol Table

lexer = lex.lex()
yacc.yacc()

f = open("test.asm", 'r')
lines = f.read().split('\n')

# .ORIG Check
assert(not (lines[0].split()[0] == '.ORIG' and re.match(r'[xX][-]?[0-9a-fA-F]+', lines[0].split()[1]) and len(lines) == 2))

# ------------ PASS ONE ------------

line_counter = int(lines[0].split()[1][1:], 16)
assert(line_counter >= 0 and line_counter < 65535)

for line in lines[1:]:
	pre_split = line.split()
	if pre_split[0] == '.END':
		break

	if not isOpcode(pre_split[0]):
		symbols[pre_split[0]] = line_counter

	line_counter = line_counter + 1


print "=== Symbol Table ==="
for symbol in symbols:
	print symbol, ':', hex(symbols[symbol])


# ------------ PASS TWO ------------
print "\n=== Result === "
line_counter = int(lines[0].split()[1][1:], 16)

for line in lines[1:]:
	pre_split = line.split()
	if pre_split[0] == '.END':
		break
	# Label Processing
	for i in range(1, len(pre_split)):
		if pre_split[i] in symbols:
			pre_split[i] = '#-8'
	# print pre_split
	if isOpcode(pre_split[0]):
		print yacc.parse(' '.join(pre_split))
	else:
		print yacc.parse(' '.join(pre_split[1:]))
	line_counter = line_counter + 1

# .END Check
assert(lines[-1].split()[0] == '.END' and len(lines[-1].split()) == 1)