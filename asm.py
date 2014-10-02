# Assembler for LC-3 ISA
# Input: .asm
# Output: .obj
import sys

# File Preparation
fSource = open(sys.argv[1], 'r')
# fSymbol = open(sys.argv[1][:-3] + 'sym', 'w')
# fBinary = open(sys.argv[1][:-3] + 'bin', 'w')

# Knowledge Table
instructions = ['ADD', 'AND', 'NOT', 'BRnzp', 'BRn', 'BRz', 'BRp', 'BRnz', 'BRnp', 'BRzp', 'JMP', 'RET', 'JSR', 'JSRR', 'LD', 'LDI', 'LDR', 'LEA', 'RTI', 'ST', 'STI', 'STR', 'TRAP', 'HALT']
directives = ['.FILL', '.BLKW', 'STRINGZ']

# Functions
def processDirective(array, LC):
	if array[0] in instructions:
		return processInstruction(array, LC)
	elif array[0] == '.FILL':
		return hex2bin(array[1][1:], 16)

def hex2bin(hex, len):
	return bin(int(hex, 16))[2:].zfill(len)	

def getReg(str):
	return bin(int(str[1]))[2:].zfill(3)


def toArr(str):
	return map(lambda x:x, str)

def transform(original):
	notTable = {'0' : '1', '1' : '0'}
	length = len(original)
	flag = False
	original = toArr(original)
	new = toArr(''.zfill(length))

	for i in range(length):
		back = length - 1 - i
		origBit = original[back]

		new[back] = notTable[origBit] if flag else origBit
		if (not flag) and origBit == '1':
			flag = True
			continue

	return ''.join(new)

def get2com(str, len):
	# Get 2's complament in binary form for signed hexadecimal
	# Input: 'x1' or 'x-3'
	# Output (len=5): '00001' or '11101'
	return transform(hex2bin(str[2:], len)) if str[1] == '-' else hex2bin(str[1:], len)

def getOffset(string, LC, len):
	if string[0] == 'x':
		offset = string
	else:
		offset = symbolTable[string] - LC - 1
		offset = hex(offset)[1:] if offset >= 0 else 'x-' + str(hex(-offset))[2:]
	return get2com(offset, len)

def dec2bin(val, len):
	return bin(val)[2:].zfill(len)

def processInstruction(array, LineCounter):
	commentStart = -1
	for i in range(len(array)): # Comment
		if array[i][0] == ';':
			commentStart = i
			break
	if commentStart != -1:
		array = array[:commentStart]
			

	if array[0] == 'LD':

		DR = getReg(array[1])
		PCoffset = getOffset(array[2], LineCounter, 9)
		return '0010' + DR + PCoffset

	elif array[0] == 'ADD':

		DR  = getReg(array[1])
		SR1 = getReg(array[2])
		tail = '000' + getReg(array[3]) if array[3][0] == 'R' else '1' + get2com(array[3], 5)
		return '0001' + DR + SR1 + tail

	elif array[0] == 'ST':

		SR = getReg(array[1])
		PCoffset = getOffset(array[2], LineCounter, 9)
		return '0011' + SR + PCoffset

	elif array[0] == 'HALT':

		return '1111000000100101'

	elif array[0] == 'AND':

		DR  = getReg(array[1])
		SR1 = getReg(array[2])
		tail = '000' + getReg(array[3]) if array[3][0] == 'R' else '1' + get2com(array[3], 5)
		return '0001' + DR + SR1 + tail

	elif array[0] == 'LEA':

		DR = getReg(array[1])
		PCoffset = getOffset(array[2], LineCounter, 9)
		return '1110' + DR + PCoffset

	elif array[0][:2] == 'BR':
		conditions = toArr(array[0][2:])
		nzp = 0
		dic = { 'n' : 4, 'z' : 2, 'p' : 1}
		for ch in conditions:
			nzp += dic[ch]

		nzp = dec2bin(nzp, 3)
		PCoffset = getOffset(array[1], LineCounter, 9)
		return '0000' + nzp + PCoffset

	elif array[0] == 'LDR':
		DR = getReg(array[1])
		BR = getReg(array[2])
		PCoffset = getOffset(array[3], LineCounter, 6)
		return '0110' + DR + BR + PCoffset;

	else:
		return ''.join(array)

# First Pass: Build Symbol Table

# Initialiazation
content = fSource.read().split('\n')
for i in range(len(content)):
	if content[i].find('.ORIG') != -1:
		startLineNumber = i
	if content[i].find('.END') != -1:
		endLineNumber = i
		break

if startLineNumber >= endLineNumber:
	sys.exit()

startPosition = content[startLineNumber].split()[1]

LineCounter = int(startPosition[1:],16)
headLine = bin(LineCounter)[2:].zfill(16)

content = content[startLineNumber+1 : endLineNumber]
symbolTable = {}

newContent = []

print '---------PASS ONE------------'
for line in content:
	line = line.split()

	if not line[0] in instructions:
		if not line[0] in directives:
			symbolTable[line[0]] = LineCounter
			line = line[1:]
		line = processDirective(line, LineCounter)


	print hex(LineCounter)[1:], ':\t\t', line
	newContent.append(line)
	LineCounter += 1

print '-------Symbol Table----------'
print symbolTable

# Initialization
content = newContent
newContent = []
LineCounter = int(startPosition[1:],16)

print '---------PASS TWO------------'
for line in content:
	if not type(line) is 'str': # Not assembled yet
		line = processInstruction(line, LineCounter)
	print hex(LineCounter)[1:], ':\t\t', line

	newContent.append(line)
	LineCounter += 1

newContent.insert(0, headLine)

print '-----------RESULT------------'
print '\n'.join(newContent)