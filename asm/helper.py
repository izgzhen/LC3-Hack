def findLineContaining(list, target):
	for i in range(len(list)):
		if list[i].find(target) != -1:
			return i

	return -1

def getOffset(string, LC, len):
	if string[0] == 'x':
		offset = string
	else:
		offset = symbolTable[string] - LC - 1
		offset = hex(offset)[1:] if offset >= 0 else 'x-' + str(hex(-offset))[2:]
	return transformer.get2com(offset, len)

def getReg(str):
	return transformer.bin(int(str[1]))[2:].zfill(3)