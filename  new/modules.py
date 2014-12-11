import resource
import transformer
'''
New Modules:
	Basic:
		Wire -- Calling Tube
		Buffer -- Behave like Flipflop, various width
		Latch -- Single bit data storing

	Complex:
		Memory -- Addressing I/O, WE + LDE <-- Buffer, Latch
		Bus -- Special support for public-reading, public-writing (writing protection)
		ALU -- Buffering operands and opcodes, supporting AND, ADD, and NOT <-- Buffer
		RegFile -- Storing registers for "rapid" accessing.
		Clock -- Send signals through driver lines every cycle
'''

class Wire(object):
	def connect(self, device):
		self.write = device.write

class Buffer(object):
	def __init__(self, length):
		self.data = '0' * length

	def connect(self, device):
		self.push = device.write 

	def write(self, data):
		self.data = data

	def sync(self):
		self.push(self.data)

class Latch(object):
	def write(self, data):
		self.data = data

class Memory(object):
	def __init__(self, wordLength, addressability):
		nullWord = '0' * wordLength
		self.space = [nullWord] * addressability
		self.MAR = Buffer(16)
		self.MDR = Buffer(16)
		self.WE  = Latch()	# Write Enable Bit
		self.LDE  = Latch() # Load Enable Bit

	def connect(self, device):
		self.output = device.write

	def sync(self):
		if self.WE.data == '1':
			self.space[transformer.toVal(self.MAR.data)] = self.MDR.data
		elif self.LDE.data == '1':
			self.MDR.data = self.space[transformer.toVal(self.MAR.data)]
			self.output(self.MDR.data)

class Bus(object):
	def __init__(self, length):
		nullWord = '0'*length
		self.data = nullWord
		self.protected = False
		self.outputs = []

	def connect(self, device):
		self.outputs.append(device.write)

	def write(self, data):
		if not self.protected:
			self.protected = True
			self.data = data

	def sync(object):
		for output in self.outputs:
			output(self.data)
		self.protected = False

class Clock(object):
	def __init__(object):
		self.outputs = []
		self.cycles = 0 	# for debugging purpose

	def sync(self):
		for output in self.outputs:
			output.write('1')
		self.cycles += 1

class ALU(object):
	def __init__(self, opMuxWidth, operandWidth, operations):
		self.opMux 	  = Buffer(opMuxWidth)
		self.operations = operations
		self.operand1 = Buffer(operandWidth)
		self.operand2 = Buffer(operandWidth)
		self.width = operandWidth

	def connect(self, output):
		self.output = output.write

	def sync(self):
		op1 = transformer.toVal(self.operand1.data)
		op2 = transformer.toVal(self.operand2.data)
		op = self.opMux.data
		result = self.operations[op](op1, op2)

		self.output(bin(result)[2:].zfill(16))

class RegFile(object):
	def __init__(self, regNum, regMuxWidth, wordLength):
		nullWord = '0' * wordLength
		self.regs = [nullWord] * regNum
		self.regMux = Buffer(regMuxWidth)
		self.WE = Latch()
		self.LDE = Latch()

	def connect(self, output):
		self.output = output.write

	def write(self, data):
		if self.WE.data == '1':
			self.regs[transformer.toVal(self.regMux.data)] = data

	def sync(self):
		self.output(self.regs[transformer.toVal(self.regMux.data)])

class FakeWire(object):
	def write(self, data):
		print data