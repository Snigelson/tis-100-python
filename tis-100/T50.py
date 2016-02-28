# T50 - File node
import sys

# I wonder. Should this node instead each tick try to read a line from the file and push the value onto the port-queue?

# I am starting to smell a possible pattern of inheritance.

# TODO: File direction!

import _node

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
			self.write(next(iter(self.in_ports.values())).get_nowait())
		elif len(self.out_ports)==1:
			port=next(iter(self.out_ports.values()))
			if port.full():
				import queue
				raise queue.Full # Ugly way of still triggering queue.Full and preserving input
			else:
				try:
					value=self.read()
				except ValueError:
					import queue
					raise queue.Empty
			next(iter(self.out_ports.values())).put_nowait(value)
		else:
			raise Exception("File has no ports!")
		
	def read(self):
		return int(self.fd.readline())
	
	def write(self, val):
		self.fd.write(str(val)+'\n')
