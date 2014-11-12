def toVal(num):
	# Not a complete version, I will upgrade it later, I am still a bad regex user
	if type(num) == type(1):
		return num
	else:
		return int(num, 2)

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
		self.space[toVal(addr)] = data # if in string format

	def at(self, addr):
		return self.space[toVal(addr)]

	def sync(self):
		if self.WE:
			self.set(self.MAR, self.MDR)
		elif self.LDE:
			self.MDR = self.at(self.MAR)

class Computer(object):
	def __init__(self):
		wordLength = 16
		nullWord = '0' * wordLength
		regNum = 8

		self.mem = Memory()
		self.PC  = 0
		self.IR  = nullWord
		self.regs = [nullWord] * regNum

		self.ops = {
		'ADD' : lambda x, y : x + y,
		'AND' : lambda x, y : x & y,
		'NOT' : lambda x 	: ~ x
	  	}

	def run(self):
		# self.mem.sync()
		while self.PC <= 10:
			self.IR = self.fetchInst()
			# print self.PC, ':', self.IR
			self.decode(self.IR)

	def evalAddr(offset):
		return PC + toVal(offset)

	def fetchOperand(addr, type):
		if type == 'r': # register
			return self.regs[addr]
		elif type == 'm':
			return self.mem[addr]

	def execute(op, operands):
		if len(operands) == 2:
			return bin(self.ops[op](toVal(operands[0]) + toVal(operands[1])))[2:]
		elif len(operands) == 1:
			return bin(self.ops[op](toVal(operands[0])))

	def store(dest, data, type):
		if type == 'r':
			self.regs[toVal(dest)] = data
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