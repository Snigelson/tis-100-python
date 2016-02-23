# tis-100.py
import sys

Debug=False

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

		# list for instructions
		self.ins = []
		
		# list for labels
		self.label = []
		
		# Original code
		self.original_code=''

		# Data read and write callbacks
		self.read_callback=None
		self.write_callback=None

	@property
	def code(self):
		return self.original_code

	@code.setter
	def code(self,text):
		self.ins=[]
		self.label=[]
		
		# save the original code
		self.original_code = text
		
		for line in text.splitlines():
			if Debug:
				print ('Line: {}'.format(line))
			
			comment_sep = line.find('#')
			line = line[0:comment_sep] if not comment_sep == -1 else line
			label_sep = line.find(':')
			label = line[0:label_sep].strip(' \t') if not label_sep == -1 else None
			line = line[label_sep+1:] if not label_sep == -1 else line
			line = line.strip(' \t')
			args=line.replace(","," ").split()
			#args=line.replace(" ",",").split(",")
			
			if Debug:
				print('Stripped: {}'.format(line))
				print('Label: {}'.format(label))
				print('Op and args: {}'.format(args))
				print('---')
			if not args==[]:
				self.ins.append(args)
				self.label.append(label)
		
		if Debug:
			print("List of labels:\n{}".format(self.label))
			print("List of instructions:\n{}".format(self.ins))
		
	def reset(self):
		'''Restart execution and reset registers'''
		self.ACC = 0
		self.BAK = 0
		self.IP = 0

	# handle errors
	def error(self,code):
		print ('ERR at instruction {}: {} ({})'.format(self.IP + 1, errors[code], code))
	
	def exec_next(self):
		self.execute(self.IP)

	def execute(self, IP):
		if Debug:
			print("Executing: {}".format(self.ins[IP]))
		opcode=self.ins[IP][0]
		arg=self.ins[IP][1:]
		is_jump_op=False
		
		if opcode == 'NOP':
			pass
	
		elif opcode == 'MOV':
			val = self._read(arg[0])
			self._write(arg[1],val)
	
		elif opcode == 'SWP':
			self.ACC, self.BAK = self.BAK, self.ACC

		elif opcode == 'SAV':
			self.BAK = self.ACC

		elif opcode == 'ADD':
			val = self._read(arg[0])
			self.ACC += val

		elif opcode == 'SUB':
			val = self._read(arg[0])
			self.ACC -= val

		elif opcode == 'NEG':
			self.ACC = int(-self.ACC)

		elif opcode == 'JMP':
			is_jump_op=True
			try:
				self.IP = self.label.index(arg[0])
			except:
				self.error(0x03)

		elif opcode == 'JEZ':
			if self.ACC == 0:
				is_jump_op=True
				try:
					self.IP = self.label.index(arg[0])
				except:
					self.error(0x03)

		elif opcode == 'JNZ':
			if self.ACC != 0:
				is_jump_op=True
				try:
					self.IP = self.label.index(arg[0])
				except:
					self.error(0x03)

		elif opcode == 'JGZ':
			if self.ACC > 0:
				is_jump_op=True
				try:
					self.IP = self.label.index(arg[0])
				except:
					self.error(0x03)

		elif opcode == 'JLZ':
			if self.ACC < 0:
				is_jump_op=True
				try:
					self.IP = self.label.index(arg[0])
				except:
					self.error(0x03)

		elif opcode == 'JRO':
			is_jump_op=True
			val = self._read(arg[0])
			try:
				self.IP += val
			except:
				self.error(0x04)
			self.IP=max(self.IP,0)
			self.IP=min(self.IP,len(self.ins)-1)

		# if none of the above, must be an invalid instruction
		else:
			self.error(0x01)
		
		if not is_jump_op:
			self.IP+=1
			self.IP %= len(self.ins)

	def _read(self, source):
		'''Read a value.'''
		if source=='NIL':
			return 0
		elif source=='ACC':
			return self.ACC
		elif source=='IN':
			import sys
			return int(sys.stdin.readline())
		else:
			return int(source)

	def _write(self, dest, val):
		if dest == 'ACC':
			self.ACC = val
		elif dest == 'OUT':
			import sys
			sys.stdout.write(str(val)+'\n')
		elif dest == 'NIL':
			pass
		else:
			self.error(0x02)

if __name__=="__main__":
	with open(sys.argv[1]) as f:
		code = f.read()

	tis=tis_node()
	tis.code=code

	while True:
		tis.exec_next()
