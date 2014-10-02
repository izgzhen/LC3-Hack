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
	arr = []
	for i in str:
		arr.append(i)
	return arr

def transform(original):
	notTable = {'0' : '1', '1' : '0'}
	length = len(original)
	flag = False
	new = ''.zfill(length)
	original = toArr(original)
	new = toArr(original)
	for i in range(length):
		if flag:
			new[length - 1 - i] = notTable[original[length - 1- i]]
		else:
			new[length - 1 - i] = original[length - 1- i]
		if (not flag) and original[length - 1 - i] == '1':
			flag = True
			continue
	return ''.join(new)

def get2com(str, len):
	# Input: 'x1' or 'x-3'
	# Output (len=5): '00001' or '11101'
	if str[1] == '-':
		print str
		binary = hex2bin(str[2:], len);
		binary = transform(binary);
		return binary
	else:
		binary = hex2bin(str[1:], len);
		return binary

def getOffset(string, LC, len):
	if string[0] == 'x':
		offset = string
	else:
		offset = symbolTable[string] - LC - 1
		if offset >= 0:
			offset = hex(offset)[1:]
		else:
			offset = 'x-' + str(hex(-offset))[2:]
	return get2com(offset, len)

def processInstruction(array, LineCounter):
	commentStart = -1
	for i in range(len(array)): # Comment
		if array[i][0] == ';':
			commentStart = i
			break
	if commentStart != -1:
		array = array[:commentStart]
			

	if array[0] == 'LD':

		DR = bin(int(array[1][1]))[2:].zfill(3)
		PCoffset = getOffset(array[2], LineCounter, 9)

		return '0010' + DR + PCoffset

	elif array[0] == 'ADD':

		DR  = getReg(array[1])
		SR1 = getReg(array[2])

		if array[3][0] == 'R': # Register Mode
			SR2 = getReg(array[3])
			return '0001' + DR + SR1 + '000' + SR2
		else: # Immediate Mode
			IMM = get2com(array[3], 5)
			return '0001' + DR + SR1 + '1' + IMM;

	elif array[0] == 'ST':

		SR = getReg(array[1])
		PCoffset = getOffset(array[2], LineCounter, 9)

		return '0011' + SR + PCoffset

	elif array[0] == 'HALT':

		return '1111000000100101'

	elif array[0] == 'AND':

		DR  = getReg(array[1])
		SR1 = getReg(array[2])

		if array[3][0] == 'R': # Register Mode
			SR2 = getReg(array[3])
			return '0101' + DR + SR1 + '000' + SR2
		else: # Immediate Mode
			IMM = get2com(array[3], 5)
			return '0101' + DR + SR1 + '1' + IMM;

	elif array[0] == 'LEA':

		DR = getReg(array[1])
		PCoffset = getOffset(array[2], LineCounter, 9)

		return '1110' + DR + PCoffset

	elif array[0][:2] == 'BR':
		conditions = []
		for i in array[0][2:]:
			conditions.append(i)

		nzp = 0
		if 'n' in conditions:
			nzp += 4
		if 'z' in conditions:
			nzp += 2
		if 'p' in conditions:
			nzp += 1
		nzp = bin(nzp)[2:].zfill(3)

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
header = bin(LineCounter)[2:].zfill(16)

content = content[startLineNumber+1 : endLineNumber]
symbolTable = {}

newContent = []

print '---------PASS ONE------------'
for line in content:
	line = line.split()

	if not line[0] in instructions:
		if not line[0] in directives:
			symbolTable[line[0]] = LineCounter
			line = processDirective(line[1:], LineCounter)
		else:
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

newContent.insert(0, header)

print '-----------RESULT------------'
print '\n'.join(newContent)







