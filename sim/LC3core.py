import transformer
import modules
import fsm

class Computer(object):
	def __init__(self):
		wordLength = 16
		nullWord = '0' * wordLength
		regNum = 8

		self.mem = modules.Memory()
		self.PC  = 0
		self.IR  = nullWord
		self.regs = [nullWord] * regNum
		self.N = self.Z = self.P = '0'

		self.fsm = fsm.FSM({
			18 : { 'default' : 33 },
			33 : { 'default' : 35 },
			35 : { 'default' : 32 },
			32 : { 'default' : 'operate' },
			'operate' : { 'default' : 'store' },
			'store' : { 'default' : 18 }
			}, initialState = 18, hasOutput = False)

		self.actionMux = {
			18 : self.fetchInst,
			33 : self.mem.sync,
			35 : self.loadIR,
			32 : self.decode,
			'operate' : self.operate,
			'store' : self.store
		}

		self.ALU = {
		'ADD' : lambda x, y : x + y,
		'AND' : lambda x, y : x & y,
		'NOT' : lambda x 	: ~ x
	  	}

		self.clk = modules.Clock()

	def run(self):
		while self.PC <= 10:
			print 'R1', self.regs[1]
			self.actionMux[self.fsm.state]()

	def fetchInst(self):
		self.mem.MAR = self.PC
		self.mem.LDE = True
		self.PC += 1

	def loadIR(self):
		self.mem.LDE = False
		self.IR = self.mem.MDR

		# For Debug
		self.IR = '0001' + '1'*12

	def decode(self):
		# For Debug
		opcodes = {
			'0001' : 'ADD',
			'0101' : 'AND',
			'1001' : 'NOT'
		}

		self.opMux = opcodes[self.IR[0:4]]
		self.operands = ['0001', '0010']
		self.dest = ['001', 'r']

	def evalAddr(offset):
		return self.PC + transformer.toVal(offset)

	def fetchOperand(addr, type):
		if type == 'r':
			return self.regs[addr]
		elif type == 'm':
			return self.mem[addr]

	def operate(self):
		op = self.opMux

		if len(self.operands) == 2:
			self.result = bin(self.ALU[op](transformer.toVal(self.operands[0]), transformer.toVal(self.operands[1])))[2:].zfill(16)
		elif len(self.operands) == 1:
			self.result = bin(self.ALU[op](transformer.toVal(self.operands[0])))[2:].zfill(16)

	def store(self):
		dest = self.dest[0]
		type = self.dest[1]
		if  type == 'r':
			self.regs[transformer.toVal(dest)] = self.result
		elif type == 'm':
			self.writeMem(dest, self.result)

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