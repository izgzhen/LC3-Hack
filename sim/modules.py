import transformer

class Memory(object):
	# I need access control here
	def __init__(self):
		wordLength = 16
		addressability = pow(2, 16)
		nullWord = '0' * wordLength

		self.space = [nullWord] * addressability
		self.MAR = nullWord
		self.MDR = nullWord
		self.WE  = False	# Write Enable Bit
		self.LDE  = False	# Load Enable Bit

	def set(self, addr, data):
		self.space[transformer.toVal(addr)] = data # if in string format

	def at(self, addr):
		return self.space[transformer.toVal(addr)]

	def sync(self):
		if self.WE:
			self.set(self.MAR, self.MDR)
		elif self.LDE:
			self.MDR = self.at(self.MAR)