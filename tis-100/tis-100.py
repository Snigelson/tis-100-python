import sys
import T21
import T50
import queue
import threading

class TIS_100:
	def __init__(self):
		# Nodes
		self.nodes={}
		
		# Clock tick
		self.tick=threading.Condition()
	
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

	def _exec_on_tick(self, func, _tick):
		while True:
			with _tick:
				_tick.wait()
			func()

	def start(self):
		for node in self.nodes:
			t = threading.Thread(name=str(node), target=self._exec_on_tick, args=(self.nodes[node].exec_next,self.tick))
			t.start()

	def exec_one(self):
		with self.tick:
			self.tick.notify_all()

if __name__=="__main__":
	import time
	import sys
	
	tis=TIS_100()
	if False:
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
		
	if True:
		with open("../test.100") as f:
			tcode = f.read()

		tis.add_T21_node('test_node',tcode)
		tis.add_T50_node('stdin_node', sys.stdin)
		tis.add_T50_node('stdout_node', sys.stdout)
		tis.add_port('stdin_node','foo','test_node','IN')
		tis.add_port('test_node','OUT','stdout_node','bar')
	
	tis.start()
	
	while True:
		tis.exec_one()
		print("tick")
		time.sleep(0.2)
