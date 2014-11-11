'''
# Helper Functions
helper.getReg : given 'R1' output '001'
helper.getOffset : given string, LC and required length, output binary offset

# Director Functions
direc.processDirective : process (possible) directives in PASS ONE
inst.processInstruction : process info.instructions with string, LC, and len
'''

import transformer
import helper

def processInstruction(array, LineCounter):
	commentStart = -1
	for i in range(len(array)): # Comment
		if array[i][0] == ';':
			commentStart = i
			break
	if commentStart != -1:
		array = array[:commentStart]

	if array[0] == 'LD':
		# Output format: '0010' + DR + PCoffset
		# Input format: { DR:1, PCoffset: 2,9 }
		DR = helper.getReg(array[1])
		PCoffset = helper.getOffset(array[2], LineCounter, 9)
		return '0010' + DR + PCoffset

	elif array[0] == 'ADD':
		# OF: '0001' + DR + SR1 + tail
		# IF: { DR:1, SR1:2, tail: ... }
		# Problem: should I split the logic here, or left it with other parts?
		DR  = helper.getReg(array[1])
		SR1 = helper.getReg(array[2])
		tail = '000' + helper.getReg(array[3]) if array[3][0] == 'R' else '1' + transformer.get2com(array[3], 5)
		return '0001' + DR + SR1 + tail

	elif array[0] == 'ST':

		SR = helper.getReg(array[1])
		PCoffset = helper.getOffset(array[2], LineCounter, 9)
		return '0011' + SR + PCoffset

	elif array[0] == 'HALT':
		# OF: '1111000000100101'
		# IF: NULL
		return '1111000000100101'

	elif array[0] == 'AND':

		DR  = helper.getReg(array[1])
		SR1 = helper.getReg(array[2])
		tail = '000' + helper.getReg(array[3]) if array[3][0] == 'R' else '1' + transformer.get2com(array[3], 5)
		return '0001' + DR + SR1 + tail

	elif array[0] == 'LEA':

		DR = helper.getReg(array[1])
		PCoffset = helper.getOffset(array[2], LineCounter, 9)
		return '1110' + DR + PCoffset

	elif array[0][:2] == 'BR':
		conditions = toArr(array[0][2:])
		nzp = 0
		dic = { 'n' : 4, 'z' : 2, 'p' : 1}
		for ch in conditions:
			nzp += dic[ch]

		nzp = dec2bin(nzp, 3)
		PCoffset = helper.getOffset(array[1], LineCounter, 9)
		return '0000' + nzp + PCoffset

	elif array[0] == 'LDR':
		DR = helper.getReg(array[1])
		BR = helper.getReg(array[2])
		PCoffset = helper.getOffset(array[3], LineCounter, 6)
		return '0110' + DR + BR + PCoffset

	elif array[0] == 'JMP':
		BR = helper.getReg(array[1])
		return '1100' + '000'+ BR + '000000'

	elif array[0] == 'RET':
		return '1100000111000000'

	elif array[0] == 'NOT':
		DR = helper.getReg(array[1])
		SR = helper.getReg(array[2])
		return '1001' + DR + SR + '111111'

	elif array[0] == 'JSR':
		PCoffset = helper.getOffset(array[1], LineCounter, 11)
		return '0100' + '1' + PCoffset

	elif array[0] == 'JSRR':
		BR = helper.getReg(array[1])
		return '0100' + '000' + BR + '000000'
	else:
		return ''.join(array)