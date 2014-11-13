import transformer
import modules

def decoder(inst):
	dispatch = {
	'0001' : lambda args : ['ADD', ['r', args[0:2]], [ ['r', args[3:5]], ['r', args[9:11]] ]]
	}

	opcode = inst[0:3]
	args   = inst[4:15]
	return dispatch[opcode, args]


class Computer(object):
	def __init__(self):
		wordLength = 16
		nullWord = '0' * wordLength
		regNum = 8

		self.mem = modules.Memory()
		self.PC  = 0
		self.IR  = nullWord
		self.regs = [nullWord] * regNum
		self.N = self.Z = self.P = '0' # Condition Code

		self.ALU = {
		'ADD' : lambda x, y : x + y,
		'AND' : lambda x, y : x & y,
		'NOT' : lambda x 	: ~ x
	  	}

	def run(self):
		# self.mem.sync()
		while self.PC <= 10:
			self.IR = self.fetchInst()
			# print self.PC, ':', self.IR
			self.decode()


	def evalAddr(offset):
		return PC + transformer.toVal(offset)

	def fetchOperand(addr, type):
		if type == 'r': # register
			return self.regs[addr]
		elif type == 'm':
			return self.mem[addr]

	def execute(op, operands):
		if len(operands) == 2:
			return bin(self.ALU[op](transformer.toVal(operands[0]) + transformer.toVal(operands[1])))[2:]
		elif len(operands) == 1:
			return bin(self.ALU[op](transformer.toVal(operands[0])))

	def store(dest, data, type):
		if type == 'r':
			self.regs[transformer.toVal(dest)] = data
		elif type == 'm':
			self.writeMem(dest, data)

	def fetchInst(self):
		self.PC += 1
		return self.readMem(self.PC - 1) # olf PC

	def readMem(self, addr):
		self.mem.MAR = addr
		self.mem.LDE = True
		self.mem.sync()
		self.mem.LDE = False
		return self.mem.MDR

	def writeMem(self, addr, data):
		self.mem.MAR = addr
		self.mem.MDR = data
		self.mem.WE  = True
		self.mem.sync()
		self.mem.WE  = False

lc3 = Computer()
lc3.run()