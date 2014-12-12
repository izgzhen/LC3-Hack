import Tools
from Number import Number

class CPU(object):
	def __init__(self, mem):
		self.wordLength = 16
		self.addressibility = 16

		self.gRegNum = 8
		self.gRegs = [ Number(self.wordLength) ] * self.gRegNum
		self.cRegs = Number(3, 'b000')
		self.IR = Number(self.wordLength)
		self.PC = Number(self.addressibility)

		self.writeMem = mem.write
		self.readMem = mem.read

		self.getOperands = {
			'ADDr' : ['R4-7', 'R7-10', 'R13-16'],
			'ADDimm' : ['R4-7', 'R7-10', 'I11-16'],
			'BR' : ['S4-7', 'O7-16'],
			'LD' : ['R4-7', 'O7-16']
		}

	def match(self, pattern, inst):
		rulesMatch = {
			'R' : lambda segment : int(segment, 2), # Register
			'O' : lambda segment : Number(9, 'b' + segment).SEX(self.wordLength), # Offset
			'I' : lambda segment : Number(len(segment), 'b' + segment).SEX(self.wordLength), # Immediate Value
			'S' : lambda segment : segment # return the segment itself
		}
		operands = []
		for rule in pattern:
			[start, end] = rule[1:].split('-')
			operands.append(rulesMatch[rule[0]](inst.data[int(start):int(end)]))
		return operands

	def getOpcode(self, instruction):
		singleModeOpcode = {
			'0000' : 'BR',
			'0010' : 'LD'
		}

		opcode = instruction.data[0:4]
		if opcode == '0001':
			if instruction.data[10:13] == '000':
				return 'ADDr'
			elif instruction.data[10] == '1':
				return 'ADDimm'
			else:
				raise StandardError("[CPU]: Error -- Wrong ADD instruction format")
		else:
			return singleModeOpcode[opcode]

	def LD(self, DR, offset):
		SRC = self.PC.ADD(offset)
		print "[CPU]: LD", DR, "<-", SRC.hex()
		self.gRegs[DR] = self.readMem(SRC)
		return True

	def BR(self, nzp, offset):
		if Tools.match(self.cRegs.data, nzp):
			print "[CPU]: BR", offset.intCom()
			self.PC = self.PC.ADD(offset)
		return True

	def ADDr(self, DR, SR1, SR2):
		print "[CPU]: ADDr", DR, "<-", SR1, "+", SR2
		self.gRegs[DR] = Number(self.wordLength, bin(self.gRegs[SR1].int() + self.gRegs[SR2].int())[1:])
		self.setCC(DR)
		return True

	def ADDimm(self, DR, SR, Simm):
		print "[CPU]: ADDimm", DR, "<-", SR, "+", Tools.intCom(Simm.data)
		self.gRegs[DR] = self.gRegs[SR].ADD(Simm)
		self.setCC(DR)
		return True

	def step(self):
		self.IR = self.readMem(self.PC)
		self.PC = self.PC.ADD(Number(self.wordLength, 1))
		opcode = self.getOpcode(self.IR)
		if opcode:
			operands = self.match(self.getOperands[opcode], self.IR)
			# print operands
			if not apply(self.__getattribute__(opcode), operands):
				print "[CPU]: ERROR step"

	def setCC(self, index):
		if self.readRegCom(index) > 0:
			self.cRegs = Number(3, 'b001')
		elif self.readRegCom(index) == 0:
			self.cRegs = Number(3, 'b010')
		else:
			self.cRegs = Number(3, 'b100')

	def readRegCom(self, index):
		return Tools.intCom(self.gRegs[index].bin()[1:])

class Memory(object):
	def __init__(self):
		self.wordLength = 16
		self.addressibility = pow(2, 16)

		self.data = [ Number(self.wordLength) ] * self.addressibility

	def read(self, addr):
		if type(addr) == type(1):
			print "[Memory]: Read at", addr % self.addressibility
			return self.data[addr % self.addressibility]
		else:
			print "[Memory]: Read at", addr.toSize(self.wordLength).int()
			return self.data[addr.toSize(self.wordLength).int()]

	def write(self, addr, value):
		if type(addr) == type(1):
			print "[Memory]: Write at", addr % self.addressibility
			self.data[addr % self.addressibility] = value
		else:
			print "[Memory]: Write at", addr.toSize(self.wordLength).int()
			self.data[addr.toSize(self.wordLength).int()] = value