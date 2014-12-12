import Tools

class Number(object):
	# The super-set of built-in int type
	# Unsigned as Default
	def __init__(self, size, value = 'b0'):
		if size > 16:
			self.size = 16
		else:
			self.size = size

		if(type(value) == type(1)):
			self.data = bin(value)[2:].zfill(size)[-self.size:]
		elif Tools.isBinary(value):
			self.data = value[1:].zfill(self.size)[-self.size:]
		elif Tools.isHex(value):
			self.data = bin(int(value[1:], 16))[-self.size:]
		elif Tools.isDec(value):
			self.data = bin(int(value[1:]))[-self.size:]
		else:
			self.data = '0' # Default
			print "[Number] Unknown value type : Number::__init__"

		self.data = self.data.zfill(self.size)

	def hex(self):
		# Strict Format
		return 'x' + hex(int(self.data, 2))[2:].zfill((self.size - 1) / 4 + 1)

	def bin(self):
		return 'b' + self.data

	def dec(self):
		return '#' + str(int(self.data, 2))

	def int(self):
		return int(self.data, 2)

	def intCom(self):
		return Tools.intCom(self.data)

	def calculate(self, operator, operand):
		return Number(min(self.size, operand.size), operator(int(self.data, 2), int(operand.data, 2)))

	def ADD(self, operand):
		return self.calculate(lambda x,y:x+y, operand)

	def XOR(self, operand):
		return Number(min(self.size, operand.size), int(self.data, 2) ^ int(operand.data, 2))

	def AND(self, operand):
		return Number(min(self.size, operand.size), int(self.data, 2) & int(operand.data, 2))

	def OR(self, operand):
		return Number(min(self.size, operand.size), int(self.data, 2) | int(operand.data, 2))

	def NOT(self):
		return Number(self.size, 'b' + reduce(lambda s, x : s + ('1' if x == '0' else '0'), self.data, ''))

	def toSize(self, newSize):
		return Number(newSize, 'b' + self.data)

	def ZEX(self, newSize): # Zero Extends
		return self.toSize(newSize)

	def SEX(self, newSize): # Sign Extends
		if newSize > self.size:
			return Number(newSize, 'b' + self.data[0] * (newSize - self.size) + self.data)
		else:
			return self.toSize(newSize) # FIX ME: Still in doubt