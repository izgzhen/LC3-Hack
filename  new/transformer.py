def toVal(num):
	# Not a complete version, I will upgrade it later, I am still a bad regex user
	if type(num) == type(1):
		return num
	else:
		return int(num, 2)