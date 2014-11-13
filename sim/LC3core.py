import transformer
import modules

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

		self.b = modules.Bus()
		self.w = modules.Wires(16)
		self.buf = modules.Buffer(16)
		self.clk = modules.Clock()
		self.dri = modules.Driver()

		# connect
		self.buf.connect(self.b, 'o')
		self.buf.connect(self.w, 'i')
		self.clk.include(self.dri)
		self.dri.connect(self.buf)

	def run(self):
		# self.mem.sync()
		# while self.PC <= 10:
			# self.IR = self.fetchInst()
			# print self.PC, ':', self.IR
			# self.decode()

		# config
		self.buf.WE = True
		print self.b.at(0, 15)
		self.w.write('1'*16)
		print self.b.at(0, 15)
		self.clk.step()
		print self.b.at(0, 15)

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