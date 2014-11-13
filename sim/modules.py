import transformer

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
		self.space[transformer.toVal(addr)] = data # if in string format

	def at(self, addr):
		return self.space[transformer.toVal(addr)]

	def sync(self):
		if self.WE:
			self.set(self.MAR, self.MDR)
		elif self.LDE:
			self.MDR = self.at(self.MAR)

class Bus(object):
	# bus is a shared object, with a internal 16-bit width status representing voltage
	def __init__(self):
		wordLength = 16
		nullWord = '0' * 16
		self.data = nullWord

	def at(self, start, end):
		return self.data[start:end]

	def write(self, data):
		assert len(data) == 16
		self.data = data

class Wires(object):
	def __init__(self, wordLength):
		self.data = '0' * wordLength
		self.hasOutput = False

	def write(self, data):
		self.data = data
		if self.hasOutput:
			self.output.write(self.data)

	def connectOut(self, device):
		self.output = device
		self.hasOutput = True


class Buffer(object):
	def __init__(self, wordLength):
		self.data = '0' * wordLength
		self.hasOutput = False
		self.hasInput = False
		self.WE = False # Write Enable

	def write(self, data):
		if self.WE:
			self.data = data

	def sync(self):
		if self.hasOutput:
			self.output.write(self.data) # Incoming data synced

	def connect(self, wires, type):
		if type == 'i':
			wires.connectOut(self)
			self.hasInput = True
		elif type == 'o':
			self.output = wires
			self.hasOutput = True

class Clock(object):
	def __init__(self):
		self.drivers = []
		self.cycles = 0

	def include(self, wire):
		# Include wire as a driver
		self.drivers.append(wire)

	def step(self):
		for wire in self.drivers:
			wire.write('1')
			self.cycles += 1

class Driver(object):
	def connect(self, device):
		self.deviceSync = device.sync # Method Address

	def write(self, data):
		if transformer.toVal(data) > 0:
			self.deviceSync()

def decoder(inst):
	dispatch = {
	'0001' : lambda args : ['ADD', ['r', args[0:2]], [ ['r', args[3:5]], ['r', args[9:11]] ]]
	}
	opcode = inst[0:3]
	args   = inst[4:15]
	return dispatch[opcode, args]