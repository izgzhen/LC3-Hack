'''
# Basic Functions
hex2bin : given hex like 'ABC' and output length requirement like '8', output binary form
get2com & transform : Get 2's complament in binary form for signed hexadecimal 
dec2bin : given a integer and output length requirement, output binary form
toArr : transform a string into character array

Definations:
According to LC3 convention and Python built-in convention:

Literal
* Hexadecimal 	([xX]|0x)[0-9aAbBcCdDeEfF]+
* Decimal		#?[01]+
* Binary 		([bB]|0b)[0-9]

Negative Value problem:

The tricky stuff is that in Python representation, the '-' is put before '0x', '0b'; but in LC-3 convention, 
the '-' sign is put just after the 'x' or '#' or 'b'.  So it might be a problem when transforming the value.

If we have literal value, we can transform them into the 'decimal' value and do more conversions
or arithmetic operations.

We will conventionally name them hex, dec, bin, and val in funciton naming, and use h d b val as variable name.

'''

############ Number System Conversion ############

''' From String to Integer '''
def hex2val(hex):
	return int(h[1:], 16)

def bin2val(bin):
	return int(b[1:], 2)

def dec2val(dec):
	return int(d)

''' From Integer to String '''
def val2hex(val, length):
	return hex(val)[2:].zfill(length)

def val2bin(val, length):
	return bin(val)[2:].zfill(length)

def val2dec(val, len):
	return str(val).zfill(length)

''' From String to String '''
def hex2bin(h, length):
	return val2bin(hex2val(h), length)

############# Extension ###################
def SEXT(b, length):
	if bin2val(b) >= 0:
		return ZEXT(b, length)
	else
		return ONEXT(b, length)

def ZEXT(b, length):
	return b.zfill(b)

def ONEXT(b, length):
	return b if len(b) >= length else '1'*(length - len(b)) + b

############# 2's Complement #############

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
	'''
		Get 2's complament in binary form for signed hexadecimal
		Input: 'x1' or 'x-3'
		Output (len=5): '00001' or '11101' 
	'''


	return transform(hex2bin(, len)) if str[1] == '-' else hex2bin(str[1:], len)

def toArr(str):
	return map(lambda x:x, str)