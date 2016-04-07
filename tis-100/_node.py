# Base class for nodes

class _node:
	def __init__(self):
		'''Initialize node.'''
		self.name=''
		self.in_ports={}
		self.out_ports={}

	def __str__(self):
		return super().__str__()

	def add_in_port(self, name, queue):
		self.in_ports[name]=queue

	def add_out_port(self, name, queue):
		self.out_ports[name]=queue

	def exec_next(self):
		raise NotImplementedError

	def read(self):
		raise NotImplementedError

	def write(self, val):
		raise NotImplementedError

	def _read_port(self, port):
		val=port.get()
		port.task_done()
		return val

	def _write_port(self, port, value):
		port.put(value)
		port.join()
