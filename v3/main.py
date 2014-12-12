from Number import Number
import Tools
import Core

class Computer(object):
	def __init__(self):
		self.mem = Core.Memory()
		self.cpu = Core.CPU(self.mem)
		self.instNum = 0

	def load(self, filename):
		f = open(filename, 'r')
		buf = f.read().split()
		orig = int(buf[0])
		self.cpu.PC = Number(16, orig)
		print "Loading instructions: "
		for inst in buf[1:]:
			# print inst
			self.mem.write(orig, Number(16, 'b' + inst))
			orig += 1

		self.instNum = len(buf) - 1

	def run(self):
		for i in range(10):
			self.cpu.step()


LCX = Computer()
LCX.load("test.bin")
LCX.run()