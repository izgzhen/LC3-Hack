'''
	The Core of LC-3:
		1. Load Resource and inititalize Modules
		2. Config Modules
		3. Start the clock
'''

import resource
import modules

class Core(object):
	def __init__():
		self.loadModules()
		self.config()

	def initModules():
		self.mem = modules.Memory(resource.wordLength, resource.addressability)
		self.fsm = modules.FSM(resource.FSMTable)
		self.clk = modules.Clock()
		self.alu = modules.ALU(resource.operations)
		self.reg = modules.RegFile(resource.regNum, resource.regMuxWidth, resource.wordLength)
		self.bus = modules.Bus(resource.wordLength)

	def config():
		self.bus.connect(self.mem)
		self.bus.connect(self.ALU)
		self.bus.connect(self.RegFile)

		self.clk.connect(self.Memory)
		self.clk.connect(self.fsm)
		self.clk.connect(self.RegFile)

	def run():
		while True:
			self.clock.sync()