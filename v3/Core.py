from Number import Number

class CPU(object):
	def __init__(self, mem):
		self.wordLength = 16
		self.addressibility = 16

		self.gRegNum = 8
		self.gRegs = [ Number(self.wordLength) ] * self.gRegNum
		self.cRegs = { 'N' : Number(1), 'Z' : Number(1), 'P' : Number(1)}
		self.IR = Number(self.wordLength)
		self.PC = Number(self.addressibility)

		self.writeMem = mem.write
		self.readMem = mem.read

		self.operations = {
			'ADD' : lambda operands : operands[0] + operands[1]
		}


	def getOperands(self, instruction):
		return [ Number(1), Number(2) ]

	def step(self):
		self.IR = self.readMem(self.PC)
		self.PC += 1
		opcode = self.getOpcode(self.IR)
		if opcode:
			operands = self.getOperands(self.IR)
			if not self.operations[opcode](operands):
				print "[CPU]: ERROR step"

class Memory(object):
	def __init__(self):
		self.wordLength = 16
		self.addressibility = pow(2, 16)

		self.data = [ Number(self.wordLength) ] * self.addressibility

	def read(self, addr):
		print "[Memory]: Read at", addr.toSize(self.wordLength).int()
		return self.data[addr.toSize(self.wordLength).int()]

	def write(self, addr, value):
		print "[Memory]: Write at", addr.toSize(self.wordLength).int()
		self.data[addr.toSize(self.wordLength).int()] = value