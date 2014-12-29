# FIX ME : Need to judge if the content is also legitimate

def isBinary(value):
	# Not Good
	return value[0] == 'b'

def isHex(value):
	return value[0] == 'x' or value[0] == 'X' 

def isDec(value):
	return value[0] == '#'

#############################################

def flip(str):
	return ''.join(map(lambda x : '1' if x == '0' else '0', str))

def chop(str, size, tail = '0'):
	# Chop str into string array with fixed size
	# Use tail to fill the gap
	assert(len(tail) == 1)
	segments = (len(str) - 1 ) / size + 1
	if len(str) % size != 0:
		segments -= 1
	arr = []
	for i in range(segments):
		arr.append(str[i * size : (i + 1) * size])
	if len(str) % size != 0:
		arr.append(str[segments * size:] + tail * ((segments + 1) * size - len(str)))

	return arr

def match(str1, str2):
	assert(len(str1) == len(str2))
	if (int(str1) & int(str2)) != 0:
		return True
	else:
		return False

#############################################

def intCom(str):
	# Get the integer with 2's complement representation
	assert(len(str) > 2)
	if str[0] == '1':
		return - (int(flip(str[1:]), 2) + 1)
	else:
		return int(str[1:], 2)

def chToNum(ch):
	# transform char to ASCII byte in 16 bits
	binary = bin(ord(ch))[2:]
	binary = 'b' + '0' * (16 - len(binary)) + binary
	return binary