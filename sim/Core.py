import Tools
import ISA
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
			'ANDr' : ['R4-7', 'R7-10', 'R13-16'],
			'ANDimm' : ['R4-7', 'R7-10', 'I11-16'],
			'BR' : ['S4-7', 'O7-16'],
			'LD' : ['R4-7', 'O7-16'],
			'ST' : ['R4-7', 'O7-16'],
			'NOT' : ['R4-7', 'R7-10'],
			'JMP' : ['R7-10'],
			'JSR' : ['O5-16'],
			'JSRR' : ['R7-10'],
			'LDI' : ['R4-7', 'O7-16'],
			'LDR' : ['R4-7','R7-10', 'O10-16'],
			'LEA' : ['R4-7', 'O7-16']
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
			'0010' : 'LD',
			'0011' : 'ST',
			'1001' : 'NOT',
			'1100' : 'JMP',
			'1010' : 'LDI',
			'0110' : 'LDR',
			'1110' : 'LEA'
		}

		opcode = instruction.data[0:4]
		if opcode == '0001':
			if instruction.data[10:13] == '000':
				return 'ADDr'
			elif instruction.data[10] == '1':
				return 'ADDimm'
			else:
				raise StandardError("[CPU]: Error -- Wrong ADD instruction format")
		if opcode == '0101':
			if instruction.data[10:13] == '000':
				return 'ANDr'
			elif instruction.data[10] == '1':
				return 'ANDimm'
			else:
				raise StandardError("[CPU]: Error -- Wrong AND instruction format")
		if opcode == '0100':
			if instruction.data[4] == '1':
				return 'JSR'
			elif instruction.data[4:7] == '000':
				return 'JSRR'
			else:
				raise StandardError("[CPU]: Error -- Wrong AND instruction format")
		else:
			return singleModeOpcode[opcode]

	def step(self):
		self.IR = self.readMem(self.PC)
		self.PC = self.PC.ADD(Number(self.wordLength, 1))
		opcode = self.getOpcode(self.IR)

		# print '[CPU]: IR', self.IR.bin()
		if opcode:
			operands = self.match(self.getOperands[opcode], self.IR)
			apply(self.__getattribute__(opcode), operands)
		else:
			print "[CPU]: Error: Invalid Opcode"

	def setCC(self, index):
		if self.readRegCom(index) > 0:
			self.cRegs = Number(3, 'b001')
		elif self.readRegCom(index) == 0:
			self.cRegs = Number(3, 'b010')
		else:
			self.cRegs = Number(3, 'b100')

	def readRegCom(self, index):
		return Tools.intCom(self.gRegs[index].bin()[1:])

# ----------------------- ISA -----------------------
	def LD(self, DR, offset):
		SRCaddr = self.PC.ADD(offset)
		print "[CPU]: LD", 'R' + str(DR), "<-", 'mem(' + SRCaddr.hex() + ')'
		self.gRegs[DR] = self.readMem(SRCaddr)
		self.setCC(DR)

	def BR(self, nzp, offset):
		if Tools.match(self.cRegs.data, nzp):
			self.PC = self.PC.ADD(offset)
			print "[CPU]: BR", "offset(" + str(offset.intCom()) + ")"
		else:
			print "[CPU]: BR -- 'not match'"

	def ST(self, SR, offset):
		DESTaddr = self.PC.ADD(offset)
		print "[CPU]: ST", 'R' + str(SR), "->", 'mem(' + DESTaddr.hex() + ')'
		self.writeMem(DESTaddr, self.gRegs[SR])

	def ADDr(self, DR, SR1, SR2):
		print "[CPU]: ADDr", 'R' + str(DR), "<-", 'R' + str(SR1), "+", 'R' + str(SR2)
		self.gRegs[DR] = self.gRegs[SR1].ADD(self.gRegs[SR2])
		self.setCC(DR)

	def ADDimm(self, DR, SR, Simm):
		print "[CPU]: ADDimm", 'R' + str(DR), "<-", 'R' + str(SR), "+", 'Imm(' + str(Tools.intCom(Simm.data)) + ')'
		self.gRegs[DR] = self.gRegs[SR].ADD(Simm)
		self.setCC(DR)

	def ANDr(self, DR, SR1, SR2):
		print "[CPU]: ANDr", 'R' + str(DR), "<-", 'R' + str(SR1), "&", 'R' + str(SR2)
		self.gRegs[DR] = self.gRegs[SR1].AND(self.gRegs[SR2])
		self.setCC(DR)

	def ANDimm(self, DR, SR, Simm):
		print "[CPU]: ANDimm", 'R' + str(DR), "<-", 'R' + str(SR), "&", 'Imm(' + str(Tools.intCom(Simm.data)) + ')'
		self.gRegs[DR] = self.gRegs[SR].AND(Simm)
		self.setCC(DR)

	def NOT(self, DR, SR):
		print "[CPU]: NOT", 'R' + str(DR), "<-", '! R' + str(SR)
		self.gRegs[DR] = self.gRegs[SR].NOT()
		self.setCC(DR)

	def JMP(self, BR):
		print "[CPU]: JMP", 'PC <-', 'R' + str(BR)
		self.PC = self.gRegs[BR]

	def JSR(self, offset):
		self.gRegs[7] = self.PC
		DESTaddr = self.PC.ADD(offset)
		self.PC = self.readMem(DESTaddr)
		print '[CPU]: JSR', 'R7 <- PC, PC <-',  'mem(' + DESTaddr.hex() + ')'

	def JSRR(self, BR):
		self.gRegs[7] = self.PC
		self.PC = self.gRegs[BR]
		print '[CPU]: JSRR', 'R7 <- PC, PC <-', 'R' + str(BR)

	def LDI(self, DR, offset):
		addr = self.PC.ADD(offset)
		self.gRegs[DR] = self.readMem(self.readMem(addr))
		print '[CPU]: LDI', 'R' + str(DR), '<- mem(mem(' + addr.hex() + '))'
		self.setCC(DR)

	def LDR(self, DR, BR, offset):
		addr = self.gRegs[BR].ADD(offset)
		self.gRegs[DR] = self.readMem(addr)
		self.setCC(DR)
		print '[CPU]: LDR', 'R' + str(DR), '<- mem(' + 'R' + str(BR) + ' + ' + offset + ')'

	def LEA(self, DR, offset):
		self.gRegs[DR] = self.PC.ADD(offset)
		self.setCC(DR)
		print '[CPU]: LEA', 'R' + str(DR), '<- PC +', str(offset.intCom())

	# def RTI(self): # RTI is still not fully understood

# ----------------------- ISA -----------------------



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