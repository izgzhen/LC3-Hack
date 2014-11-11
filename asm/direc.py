import info
import inst
import transformer

def processDirective(array, LC):
	if array[0] in info.instructions:
		return inst.processInstruction(array, LC)
	elif array[0] == '.FILL':
		return transformer.hex2bin(array[1][1:], 16)