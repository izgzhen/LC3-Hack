class Buffer(object):
	def __init__(self):
		# self.data = '0' * length
		self.data = 0
		self.hasOutput = False

	def connect(self, device):
		self.push = device.write 

	def write(self, data):
		self.data = data

	def sync(self):
		if self.hasOutput:
			self.push(self.data)

class Reg(object):
	def __init__(self):
		self.data = 0

	def write(self, data):
		# assert len(data) == 1
		self.data = data

class Adder(object):
	def __init__(self):
		self.buf1 = Buffer()
		self.buf2 = Buffer()

	def connect(self, wire):
		self.output = wire.write

	def sync(self):
		self.output(self.buf1.data + self.buf2.data) # This is another usage of buffer as a submodule

class Wire(object):
	def connect(self, device):
		self.write = device.write # Equivalent Calling

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

b = Bus()
a = Adder()
w1 = Wire()
w2 = Wire()
w3 = Wire()
r = Reg()
w1.connect(a.buf1)
w2.connect(a.buf2)
w3.connect(r)
a.connect(w3)
w1.write(12)
w2.write(23)
a.sync()

print r.data