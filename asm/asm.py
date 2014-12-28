from tokens import *
from tools import *
from rules import *

import ply.lex as lex
import ply.yacc as yacc

symbols = {} # Symbol Table

lexer = lex.lex()
yacc.yacc()

f = open("../examples/test3.asm", 'r')
lines = f.read().split('\n')

# .ORIG Check
assert(not (lines[0].split()[0] == '.ORIG' and re.match(r'[xX][-]?[0-9a-fA-F]+', lines[0].split()[1]) and len(lines) == 2))

# .END Check
assert(lines[-1].split()[0] == '.END' and len(lines[-1].split()) == 1)

# Get start address
start_addr = int(lines[0].split()[1][1:], 16)

# Strip away the .ORIG and .END
lines = lines[1:-1]

# Strip away the comments
lines = map(lambda line : line[:line.find(';')] if line.find(';') != -1 else line, lines)

# Strip away the empty lines
lines = filter(lambda line : len(line.split()), lines)

# ------------ PASS ONE : Build Symbols Table ------------

line_counter = start_addr
assert(line_counter >= 0 and line_counter < 65535)

i = 0
while 1:
	line = lines[i]
	pre_split = line.split()

	if not isOpcode(pre_split[0]):
		symbols[pre_split[0]] = line_counter
		lines[i] = ' '.join(pre_split[1:])

	pre_split = lines[i].split(' ')

	# Macros
	if pre_split[0] == '.BLKW':
		if len(pre_split) == 1:
			lines[i] = '.FILL #0'
		else:
			lines = lines[:i] + [".FILL #0"] * toInt(pre_split[1]) + lines[i+1:]


	if pre_split[0] == '.STRINGZ':
		string = re.search(r'\"([^\"]*|(\\\"))*\"', line).group()[1:-1]
		pos = 0
		newlines = []

		convertTable = {
			'n' : '\n',
			't' : '\t'
		}

		while pos < len(string):
			if string[pos] == '\\':
				ch = string[pos + 1]
				if ch in convertTable:
			 		ch = convertTable[string[pos + 1]]
			 	pos += 2
			else:
				ch = string[pos]
				pos += 1
			newlines.append(".FILL #" + str(ord(ch)))

		newlines.append(".FILL #0")
		lines = lines[:i] + newlines + lines[i+1:]

	line_counter = line_counter + 1
	i += 1
	if i >= len(lines):
		break

print "=== Symbol Table ==="
for symbol in symbols:
	print symbol, ':', hex(symbols[symbol])


# ------------ PASS TWO ------------
print "\n=== Result === "
line_counter = start_addr
print ZEX(line_counter, 16)
i = 0

while 1:
	pre_split = lines[i].split()
	# Label Processing
	for j in range(1, len(pre_split)):
		if pre_split[j] in symbols:
			pre_split[j] = '#' + str(symbols[pre_split[j]] - line_counter - 1)

	if pre_split[0] in trap_vectors and len(pre_split) == 1:
		pre_split = ['TRAP', trap_vectors[pre_split[0]]]

	# print pre_split

	# print ' '.join(pre_split), ':', yacc.parse(' '.join(pre_split))
	print yacc.parse(' '.join(pre_split))

	line_counter = line_counter + 1
	i += 1
	if i >= len(lines):
		break