class FSM(object):
	def __init__(self, LUT, initialState, hasOutput = True):
		self.state = initialState
		self.LUT = LUT
		self.step = self.stepOut if hasOutput else self.stepNonOut

	def stepOut(self, inSignal = 'default'):
		[self.state, outSignal] = self.transform(self.state, inSignal)
		return outSignal

	def stepNonOut(self, inSignal = 'default'):
		self.state = self.transform(self.state, inSignal)
		print self.state

	def transform(self, oldState, inSignal):
		return self.LUT[oldState][inSignal]