import transformer

class Memory(object):
	def __init__(self, wordLength, addressability):
		nullWord = '0' * wordLength

		self.space = [nullWord] * addressability
		self.MAR = nullWord
		self.MDR = nullWord
		self.WE  = False	# Write Enable Bit
		self.LDE  = False	# Load Enable Bit

	def set(self, addr, data):
		self.space[transformer.toVal(addr)] = data # if in string format

	def at(self, addr):
		return self.space[transformer.toVal(addr)]

	def sync(self):
		if self.WE:
			self.set(self.MAR, self.MDR)
		elif self.LDE:
			self.MDR = self.at(self.MAR)
			
class Bus(object):
	def __init__(self):
		self.outPool = []
		self.wordLength = 16

	def connect(self, device):
		self.outPool.append(device.write)

	def write(self, data):
		assert len(data) == self.wordLength
		for output in self.outPool:
			output(data)

class Wire(object):
	def connect(self, device):
		self.write = device.write

class Buffer(object):
	def __init__(self, length):
		self.data = '0' * length
		self.hasOutput = False

	def connect(self, device):
		self.push = device.write 

	def write(self, data):
		self.data = data

	def sync(self):
		if self.hasOutput:
			self.push(self.data)

class Clock(object):
	def __init__(self):
		self.drivers = []
		self.cycles = 0

	def connect(self, wire):
		self.drivers.append(wire)

	def step(self):
		for driver in self.drivers:
			driver.write('1')
			self.cycles += 1

def decoder(inst):
	dispatch = {
	'0001' : lambda args : ['ADD', ['r', args[0:2]], [ ['r', args[3:5]], ['r', args[9:11]] ]]
	}
	opcode = inst[0:3]
	args   = inst[4:15]
	return dispatch[opcode, args]