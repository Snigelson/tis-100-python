# tis-100.py
import sys

# error codes
errors={
	0x00: 'No error',
	0x01: 'Invalid instruction',
	0x02: 'Invalid register',
	0x03: 'Invalid label',
	0x04: 'Invalid offset',
	0x05: 'Blocking read', #No node connected
	0x06: 'Blocking write' #No node connected
	}

class tis_node:
	def __init__(self):
		'''Initialize TIS node.'''
		# ACC & BAK registers
		self.ACC = 0
		self.BAK = 0

		# instruction pointer
		self.IP = 0

		# list for instructions to be loaded into
		self.ins = []

	@property
	def code(self):
		return '\n'.join(self.ins)

	@code.setter
	def code(self,text):
		# load instructions into array
		self.ins = text.splitlines()

		# strip any spaces and tabs from instructions
		for i in range(len(self.ins)):
			self.ins[i] = self.ins[i].strip(' \t')

	def reset(self):
		'''Restart execution and reset registers'''
		self.ACC = 0
		self.BAK = 0
		self.IP = 0

	# handle errors
	def error(self,code):
		print ('ERR at instruction {}: {} ({})'.format(self.IP + 1, errors[code], code))

# main execution loop
	def execute(self, opcode_index):
		opcode = self.ins[opcode_index].split(' ')

		if opcode[0] == 'NOP':
			pass
	
		elif opcode[0] == 'MOV':
			if opcode[2] == 'ACC':
				self.ACC = int(opcode[1])
			elif opcode[2] == 'OUT':
				if opcode[1] == 'ACC':
					print (self.ACC)
				else:
					print (opcode[1])
			elif opcode[2] == 'NIL':
				pass
			else:
				self.error(0x02)
	
		elif opcode[0] == 'SWP':
			self.ACC, self.BAK = self.BAK, self.ACC

		elif opcode[0] == 'SAV':
			self.BAK = self.ACC

		elif opcode[0] == 'ADD':
			if opcode[1] == 'ACC':
				self.ACC += self.ACC
			else:
				self.ACC += int(opcode[1])

		elif opcode[0] == 'SUB':
			if opcode[1] == 'ACC':
				self.ACC -= self.ACC
			else:
				self.ACC -= int(opcode[1])

		elif opcode[0] == 'NEG':
			self.ACC = int(-self.ACC)

		elif opcode[0] == 'JMP':
			try:
				self.IP = self.ins.index(opcode[1] + ':')
			except:
				self.error(0x03)

		elif opcode[0] == 'JEZ':
			if self.ACC == 0:
				try:
					self.IP = self.ins.index(opcode[1] + ':')
				except:
					self.error(0x03)

		elif opcode[0] == 'JNZ':
			if self.ACC != 0:
				try:
					self.IP = self.ins.index(opcode[1] + ':')
				except:
					self.error(0x03)

		elif opcode[0] == 'JGZ':
			if self.ACC > 0:
				try:
					self.IP = self.ins.index(opcode[1] + ':')
				except:
					self.error(0x03)

		elif opcode[0] == 'JLZ':
			if self.ACC < 0:
				try:
					self.IP = self.ins.index(opcode[1] + ':')
				except:
					self.error(0x03)

		elif opcode[0] == 'JRO':
			try:
				if opcode[1] == 'ACC':
					self.IP += self.ACC
				else:
					self.IP += int(opcode[1])
			except:
				self.error(0x04)

		elif opcode[0].endswith(':'):
			# this is a label, do nothing
			pass

		elif opcode[0].startswith('#'):
			# this is a comment, do nothing
			pass

		elif opcode[0] == '':
			# this is whitespace, do nothing
			pass

		# if none of the above, must be an invalid instruction
		else:
			self.error(0x01)
		
		self.IP += 1

if __name__=="__main__":
	with open(sys.argv[1]) as f:
		code = f.read()

	tis=tis_node()
	tis.code=code

	while True:
		tis.execute(tis.IP)
	
	# iterate through list, execute instructions
#	while IP < len(ins):
#		execute(ins[IP])
#		IP += 1
