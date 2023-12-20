# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

try:
	input_lines = io.read_input_as_lines(20)
	example_lines = io.read_example_as_lines(20)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]

class Nodule:

	HIGH_SIGNALS = 0
	LOW_SIGNALS = 0
	PULSE_QUEUE = deque()
	REGISTRY = {}
	FINISHED = False

	def press_button_nodule(testing_mode=True):
		Nodule.PULSE_QUEUE.append(("broadcaster", False, "button"))
		while Nodule.PULSE_QUEUE:
			next_name, next_signal, last_name = Nodule.PULSE_QUEUE.popleft()

			# There can be Nodules that are sent signals that didn't appear in
			# our list of Nodule instructions. If we encounter a Nodule that 
			# isn't defined, give it a generic implementation at run-time... I 
			# guess!
			if next_name not in Nodule.REGISTRY.keys():
				Nodule(f"{next_name} -> ")

			Nodule.REGISTRY[next_name].input(next_signal, last_name)

			# For Part 2:
			if not testing_mode and Nodule.FINISHED: 
				return


	def reset_static_state():
		Nodule.HIGH_SIGNALS = 0
		Nodule.LOW_SIGNALS = 0
		Nodule.PULSE_QUEUE = deque()
		Nodule.REGISTRY = {}

	def __init__(self, def_str: str) -> None:
		def_str = algos.erase(def_str, "%&")
		self.name, target_def = def_str.split(" -> ")
		self.targets = target_def.split(", ")
		Nodule.REGISTRY[self.name] = self

	def input(self, signal, last_name) -> None:
		if self.name == "rx" and not signal:
			Nodule.FINISHED = True
			return
		
		if signal:
			Nodule.HIGH_SIGNALS += 1
		else:
			Nodule.LOW_SIGNALS += 1

class Broadcaster(Nodule):

	def input(self, signal, last_name) -> None:
		super().input(signal, last_name)
		for target in self.targets:
			Nodule.PULSE_QUEUE.append((target, signal, self.name))

class FlipFlip(Nodule):

	def __init__(self, def_str) -> None:
		super().__init__(def_str)
		self.state = False

	def input(self, signal, last_name) -> None:
		super().input(signal, last_name)
		if not signal:
			self.state = not self.state
			for target in self.targets:
				Nodule.PULSE_QUEUE.append((target, self.state, self.name))

class Conjunction(Nodule):

	def __init__(self, def_str: str) -> None:
		super().__init__(def_str)
		self.finalized = False
		self.incoming_connections = {}
	
	def input(self, signal, last_name) -> None:
		if not self.finalized:
			raise ValueError(f"Conjunction {self.name} was not finalized")
		
		super().input(signal, last_name)
		self.incoming_connections[last_name] = signal
		out = not all(self.incoming_connections.values())
		for target in self.targets:
			Nodule.PULSE_QUEUE.append((target, out, self.name))

	def finalize(self):
		for nodule in Nodule.REGISTRY.values():
			nodule: Nodule
			if self.name in nodule.targets:
				self.incoming_connections[nodule.name] = False
		self.finalized = True


def do_part_one_for(lines):
	Nodule.reset_static_state()

	to_finalize = []
	for definition in lines:
		if definition[0] == "b":
			Broadcaster(definition)
		elif definition[0] == "%":
			FlipFlip(definition)
		elif definition[0] == "&":
			to_finalize.append(Conjunction(definition))

	for conj in to_finalize:
		conj.finalize()

	for pushes in range(1000):
		Nodule.press_button_nodule()
	
	return Nodule.HIGH_SIGNALS * Nodule.LOW_SIGNALS

def do_part_two_for(lines):
	Nodule.reset_static_state()

	to_finalize = []
	for definition in lines:
		if definition[0] == "b":
			Broadcaster(definition)
		elif definition[0] == "%":
			FlipFlip(definition)
		elif definition[0] == "&":
			to_finalize.append(Conjunction(definition))

	for conj in to_finalize:
		conj.finalize()

	presses = 0
	while not Nodule.FINISHED:
		Nodule.press_button_nodule(False)
		presses += 1
	
	return presses

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"We've been provided with a system of electronic modules to simulate"
       	  f". What is the product of the numbers of High and Low signals sent i"
		  f"nto the system? \n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe product of high and low signals after 1000 button presses is "
		  f"{results}")
	print(f"\tWe expected: 11687500\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe product of high and low signals after 1000 button presses is "
		  f"{results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"How many times must we press the button for a single low pulse sign"
       	  f"al to be delivered to the 'rx' Module?\n")

	print(f"Unfortunately, there's no example for Part 2.\n")	

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe number of pulses to be sent is {results}\n")

def print_header():
	print("--- DAY 20: Pulse Propagation ---\n")
