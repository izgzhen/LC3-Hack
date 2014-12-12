import Tools
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

		self.getOperands = {
			'ADDr' : lambda inst : [ int(inst.data[4:7], 2), int(inst.data[7:10], 2), int(inst.data[13:16], 2) ],
			'ADDimm' : lambda inst : [ int(inst.data[4:7], 2), int(inst.data[7:10], 2), inst.data[11:16]]
		}

	def getOpcode(self, instruction):
		# No lexer
		# return self.opcodes[instruction.data[0:4]]
		opcode = instruction.data[0:4]
		if opcode == '0001':
			if instruction.data[10:13] == '000':
				return 'ADDr'
			elif instruction.data[10] == '1':
				return 'ADDimm'
			else:
				raise StandardError("[CPU]: Error -- Wrong ADD instruction format")
		else:
			return 'ELSE'

	def ADDr(self, DR, SR1, SR2):
		print "[CPU]: ADDr", DR, "=", SR1, "+", SR2
		self.gRegs[DR] = Number(self.wordLength, bin(self.gRegs[SR1].int() + self.gRegs[SR2].int())[1:])
		return True

	def ADDimm(self, DR, SR, Simm):
		print "[CPU]: ADDimm", DR, "=", SR, "+", Tools.intCom(Number(len(Simm), 'b' + Simm).SEX(self.wordLength).data)
		self.gRegs[DR] = self.gRegs[SR].ADD(Number(len(Simm), 'b' + Simm).SEX(self.wordLength))
		return True

	def step(self):
		self.IR = self.readMem(self.PC)
		self.PC = self.PC.ADD(Number(self.wordLength, 1))
		opcode = self.getOpcode(self.IR)
		if opcode:
			operands = self.getOperands[opcode](self.IR)
			# print operands
			if not apply(self.__getattribute__(opcode), operands):
				print "[CPU]: ERROR step"

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