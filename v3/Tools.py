# FIX ME : Need to judge if the content is also legitimate

def isBinary(value):
	# Not Good
	return value[0] == 'b'

def isHex(value):
	return value[0] == 'x' or value[0] == 'X' 

def isDec(value):
	return value[0] == '#'

#############################################

def chop(str, size, tail):
	# Chop str into string array with fixed size
	# Use tail to fill the gap
