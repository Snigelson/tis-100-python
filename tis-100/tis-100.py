import sys
import T21
import T50
import queue

class TIS_100:
	def __init__(self):
		# Nodes
		self.nodes={}
		
	def add_T21_node(self, name, code):
		'''Add a computation node named name, with code.'''
		new_node=T21.T21()
		new_node.name=name
		new_node.code=code
		self.nodes[name]=new_node
	
	def add_T50_node(self, name, fd):
		'''Add a file node, reading from file descriptor fd.'''
		new_node=T50.T50()
		new_node.name=name
		new_node.fd=fd
		self.nodes[name]=new_node
	
	def add_port(self, source_node, source_name, dest_node, dest_name=None):
		'''Add a port between a node and another, or a node and a file.
		If dest is a file, dest_name needs not be defined.
		'''
		try:
			new_queue=queue.Queue(maxsize=1)
			self.nodes[source_node].add_out_port(source_name, new_queue)
			self.nodes[dest_node].add_in_port(dest_name, new_queue)
		except:
			# No such node or file
			print("Trying to add invalid port.") # Lol descriptive error messages.
			raise

	def exec_one(self):
		for n in self.nodes:
			try:
				self.nodes[n].exec_next()
			except queue.Empty:
				#print("Node {} is waiting to read this cycle.".format(n))
				pass
			except queue.Full:
				#print("Node {} is waiting to writ this cycle.".format(n))
				pass
			else:
				#print("Node {} executed this cycle.".format(n))
				pass

if __name__=="__main__":
	tis=TIS_100()
	if False:
		with open(sys.argv[1]) as f:
			code = f.read()
		tis.add_T21_node('snopp',code)
		tis.add_T50_node('stdin_node', sys.stdin)
		tis.add_T50_node('stdout_node', sys.stdout)
		tis.add_port('stdin_node','foo','snopp','IN')
		tis.add_port('snopp','OUT','stdout_node','bar')
	if True:
		with open("../duplicator.100") as f:
			dcode = f.read()
		with open("../adder.100") as f:
			acode = f.read()
		tis.add_T21_node('duplicator',dcode)
		tis.add_T21_node('adder',acode)
		tis.add_T50_node('stdin_node', sys.stdin)
		tis.add_T50_node('stdout_node', sys.stdout)
		tis.add_port('stdin_node','foo','duplicator','IN')
		tis.add_port('duplicator','DOWN','adder','UP')
		tis.add_port('adder','OUT','stdout_node','bar')
		
	while True:
		tis.exec_one()
