from Number import Number
import Tools
import Core
import sys
import thread
import time

def read_key(cb):
    import termios
    import sys
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] &= ~(termios.ICANON | termios.ECHO) # c_lflags
    c = None
    try:
        termios.tcsetattr(fd, termios.TCSANOW, new)
        c = sys.stdin.read(1)
        cb(c)
    finally:
        termios.tcsetattr(fd, termios.TCSANOW, old)
    return c

def input_thread(cb):
    read_key(cb)
    thread.interrupt_main()

class Computer(object):
	def __init__(self, doDebug):
		self.cpu = Core.CPU(self.poll, self.output, self.debug, self.info)
		self.mem = self.cpu.mem
		self.buf = ''	# Output Buffer
		self.doDebug = doDebug

	def load(self, filename):
		f = open(filename, 'r')
		buf = f.read().split()
		orig = int(buf[0], 2)
		self.cpu.PC = Number(16, 'b' + buf[0])
		self.cpu.PSR = Number(16, 'b1000001000000000') # Pr = User, PL = 2, CC = 000
		self.mem.write(self.cpu.MCR, Number(16, 'b1000000000000000')) # Set the RUN Latch
		for inst in buf[1:]:
			self.mem.write(orig, Number(16, 'b' + inst))
			orig += 1

	def run(self):
		while 1:
			if self.cpu.ch != -1:
				self.cpu.interrupt('011', '10000000')
				self._continue(False)

			cmd = raw_input("> ")
			# Step over
			if cmd == "step" or len(cmd) == 0:
				if not self.cpu.step():
					self.exit()
			# Processing Input Event
			elif cmd[0] == "R":
				print cmd, ":", self.cpu.gRegs[int(cmd[1])].hex()
			elif cmd[0] == "x":
				assert(len(cmd) == 5)
				print cmd, ":", self.mem.read(Number(16, int(cmd[1:], 16))).hex()
			elif cmd == 'PC':
				print "PC:", self.cpu.PC.hex()
			elif cmd == 'PSR':
				print "PSR:", self.cpu.PSR.hex()
			elif cmd == 'flush':
				self.flush()
			elif cmd == 'continue':
				# Interrupt
				self._continue(False)
			elif cmd == 'quit':
				exit()

	def poll(self):
		self.flush()
		return raw_input("LC3 console < ")

	def output(self, ch):
		self.buf += ch

	def flush(self):
		if len(self.buf):
			print "LC3 console >", self.buf
			self.buf = ''

	def debug(self, string):
		if self.doDebug:
			print "[CPU]:", string

	def info(self, string):
		print "[CPU]:", string

	def exit(self):
		self.flush()
		print "Halting"
		exit()

	def getch(self, ch):
		self.cpu.ch = ch

	def _continue(self, interrupted):
	    if interrupted:
	        return
	    try:
			thread.start_new_thread(input_thread, tuple([self.getch]))
			while True:
				if not self.cpu.step():
					self.exit()
				self.flush()
				time.sleep(0.05)
	    except KeyboardInterrupt:
	        self._continue(True)

print "Welcome to LC3-Sim v0.9 by izgzhen"
LCX = Computer(doDebug = False)

# Loading Operating System
LCX.load("OS/trap_vector.src")
LCX.load("OS/trap_routines.src")

# Loading User Program
LCX.load("test/test9-isr.src")
LCX.load("test/test9.src")
LCX.run()