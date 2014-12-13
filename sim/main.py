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
			self.mem.write(orig, Number(16, 'b' + inst))
			orig += 1
		print

		self.instNum = len(buf) - 1

	def run(self):
		for i in range(self.instNum):
			self.cpu.step()
			print

LCX = Computer()
LCX.load("test.bin")
LCX.run()

# print LCX.cpu.readRegCom(0)
# print LCX.cpu.PC.bin()