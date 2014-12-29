from Number import Number
import Tools
import Core

class Computer(object):
	def __init__(self):
		self.mem = Core.Memory()
		self.cpu = Core.CPU(self.mem)
		self.io = Core.IO(self.mem, self.cpu.interrupt)
		self.instNum = 0
		self.buf = ""

	def load(self, filename):
		f = open(filename, 'r')
		buf = f.read().split()
		orig = int(buf[0], 2)
		self.cpu.PC = Number(16, 'b' + buf[0])
		self.cpu.PSR = Number(16, 'b1000001000000000') # Pr = User, PL = 2, CC = 000
		print "Loading instructions: "
		for inst in buf[1:]:
			self.mem.write(orig, Number(16, 'b' + inst))
			orig += 1

		self.instNum = len(buf) - 1

	def run(self):
		while 1:
			cmd = raw_input("> ")
			# Step over
			if cmd == "step" or len(cmd) == 0:
				self.cpu.step()
			# Processing Input Event
			elif cmd == "input":
				self.buf += raw_input("console < ")
				self.io.input(self.buf[0])
				self.buf = self.buf[1:]
			elif cmd[0] == "R":
				print cmd, ":", self.cpu.gRegs[int(cmd[1])].hex()
			elif cmd[0] == "x":
				assert(len(cmd) == 5)
				print cmd, ":", self.mem.read(Number(16, int(cmd[1:], 16))).hex()
			elif cmd == 'PC':
				print "PC:", self.cpu.PC.hex()
			elif cmd == 'PSR':
				print "PSR:", self.cpu.PSR.hex()
			elif cmd == 'quit':
				exit()

			# Processing Output
			output = self.io.output()
			if output:
				print "console >", output

print "Welcome to LC3-Sim v0.9 by izgzhen"
LCX = Computer()
LCX.load("test.bin")
LCX.run()