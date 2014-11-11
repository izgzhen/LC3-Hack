class memory(object):
	def __init__(self):
		wordLength = 16
		addressability = pow(2, 16)
		nullWord = '0' * wordLength
		self.mem = [nullWord] * addressability

		self.MAR = nullWord
		self.MDR = nullWord

lc3mem = memory()
print lc3mem.MDR