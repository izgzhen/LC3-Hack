from Number import Number
import Tools
import Core

class Computer(object):
	def __init__(self):
		self.mem = Core.Memory()
		self.cpu = Core.CPU(self.mem)

	def load(self, filename):
		f = open(filename, 'r')
		buf = f.read()
		buf = chop(buf, 16, '0')


LCX = Computer()

a = Number(1, 'b1')
print a.toSize(10).bin()

# print LCX.cpu.readMem(Number(17,'b10000000000000000')).int()
# LCX.cpu.writeMem(Number(16,1), Number(16, 255))
# print LCX.cpu.readMem(Number(16,1)).int()