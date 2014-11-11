import inst
import direc
import info
import helper
import assembler

class assembler(object):
	def __init__(self, src):
		self.content = open(src, 'r').read().split('\n')

		startLine = helper.findLineContaining(self.content, '.ORIG')
		endLine = helper.findLineContaining(self.content, '.END')

		if startLine == -1 or endLine <= startLine:
			sys.exit()

		startPosition = self.content[startLine].split()[1]

		self.initialLC = int(startPosition[1:],16)
		self.content = self.content[startLine + 1 : endLine]

	def passOne(self):
		LC = self.initialLC
		symbolTable = {}
		newContent = []

		print '---------PASS ONE------------'
		for line in self.content:
			line = line.split()

			if not line[0] in info.instructions:
				if not line[0] in info.directives:
					symbolTable[line[0]] = LC
					line = line[1:]
				line = direc.processDirective(line, LC)

			print hex(LC)[1:], ':\t\t', line
			newContent.append(line)
			LC += 1

		print
		print '-------Symbol Table----------'
		print symbolTable
		print

		self.content = newContent

	def passTwo(self):
		LC = self.initialLC
		newContent = []
		headLine = bin(LC)[2:].zfill(16)

		for line in self.content:
			if not type(line) is 'str': # Not assembled yet
				line = inst.processInstruction(line, LC)
			print hex(LC)[1:], ':\t\t', line

			newContent.append(line)
			LC += 1

		newContent.insert(0, headLine)

		print
		print '-----------RESULT------------'
		print '\n'.join(newContent)

	def generate(self):
		self.passOne()
		self.passTwo()