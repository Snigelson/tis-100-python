# T50 - File node
import sys
import _node
import queue

class T50(_node._node):
	def __init__(self):
		'''Initialize node.'''
		self.fd=None
		super().__init__()

	def add_in_port(self, name, queue):
		if len(self.in_ports)==1 or len(self.out_ports)==1:
			raise Exception("Too many ports for file node!")
		super().add_in_port(name, queue)

	def add_out_port(self, name, queue):
		if len(self.in_ports)==1 or len(self.out_ports)==1:
			raise Exception("Too many ports for file node!")
		super().add_out_port(name, queue)

	def exec_next(self):
		if len(self.in_ports)==1:
			port=next(iter(self.in_ports.values()))
			val=super()._read_port(port)
			self.write(val)
		elif len(self.out_ports)==1:
			port=next(iter(self.out_ports.values()))
			value=self.read()
			super()._write_port(port,value)
		else:
			raise Exception("File has no ports!")
		
	def read(self):
		return int(self.fd.readline())
	
	def write(self, val):
		self.fd.write(str(val)+'\n')
