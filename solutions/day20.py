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

	SORT_INDEX = {
		'nd': 1024, 'ql': 9, 'gz': 126, 'lg': 16382, 'tr': 9, 'vn': 17, 
		'kg': 4096, 'sj': 254, 'hf': 4094, 'vv': 67, 'gf': 513, 'zt': 4096, 
		'bm': 131, 'cp': 66, 'gs': 131, 'sp': 16382, 'bh': 17, 'xb': 33, 
		'fx': 509, 'gq': 66, 'xp': 131, 'hl': 18, 'sk': 2048, 'mh': 16382, 
		'sh': 4096, 'jh': 8191, 'gp': 8191, 'xf': 253, 'cv': 35, 'kr': 9, 
		'xz': 2052, 'fs': 516, 'xm': 2051, 'qf': 259, 'fn': 253, 'kh': 1026, 
		'vh': 16382, 'mq': 34, 'zn': 62, 'sv': 513, 'lh': 9, 'dl': 17, 
		'zx': 8195, 'pz': 2052, 'cn': 1026, 'xs': 8191, 'gb': 33, 'zs': 1026
	}

	UPDATE_ALL = 0
	UPDATE_DELTA = 1
	UPDATE_NEVER = 2

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

	def print_state_overkill(update_mode: int):
		ff_header = ""
		ff_readout = ""
		conjunction_readouts = {}

		relevant_flipflops = set()
		for nodule in Nodule.REGISTRY.values():
			if isinstance(nodule, Conjunction):
				rels = set(nodule.incoming_connections.keys())
				relevant_flipflops = relevant_flipflops.union(rels)

		# Build notes from the registry on the state of all of the flipflops and
		# conjunctions. The row of flipflops is printed as-is, whereas 
		# conjunctions are merged to one line, so we need to know their whole
		# deal first.
		for k in Nodule.REGISTRY.keys():
			if isinstance(Nodule.REGISTRY[k], FlipFlip):
				if k in relevant_flipflops:
					ff_header += f"|{k} "
					ff_readout += f"| {1 if Nodule.REGISTRY[k].state else 0} "

			if isinstance(Nodule.REGISTRY[k], Conjunction):
				conj = Nodule.REGISTRY[k]
				conj: Conjunction

				conj_header = f"|{k} "
				conj_nm_line = ""
				conj_readout = ""
				first = True

				for inc_nm, inc_bit in conj.incoming_connections.items():
					if not first: 
						conj_header += "    "
					first = False
					conj_nm_line += f"|{inc_nm} "
					conj_readout += f"| {1 if inc_bit else 0} "

				conj_header += "|"
				conj_nm_line += "|"
				conj_readout += "|"
				conj_div = "-" * len(conj_header)
				conj_ro_width = len(conj_header)
				conj_lines = [conj_header, conj_nm_line, conj_readout, conj_div]

				conjunction_readouts[k, conj_ro_width] = conj_lines
		
		# Since we can show all the flip-flops at once, we can go ahead and 
		# enqueue them. 
		ff_header += "|"
		ff_readout += "|"
		ff_div = "-" * len(ff_header)
		print_queue = [ff_div, ff_header, ff_div, ff_readout, ff_div, ""]

		# Combine Conjunction data on the same line if possible, up the length 
		# of the flipflop readout. 
		conj_queue = sorted(conjunction_readouts.keys(), key=lambda cl: cl[1])
		conj_queue.reverse()
		while conj_queue:
			cnm, clen = conj_queue.pop()
			comb_len = clen
			cnms = [(cnm, clen)]
			try:
				grab_another = comb_len + conj_queue[-1][1] + 1 < len(ff_header)
			except: 
				grab_another = False
			while len(conj_queue) and grab_another:
				next_cnm, next_clen = conj_queue.pop()
				cnms.append((next_cnm, next_clen))
				comb_len += next_clen + 1
				try:
					grab_another = comb_len + conj_queue[-1][1] + 1 < len(ff_header)
				except: 
					grab_another = False

			agg_ch = ""
			agg_cn = ""
			agg_cr = ""
			aggd = ""
			for key in cnms:
				c_h, c_n, c_r, c_d = conjunction_readouts[key]
				agg_ch += f"{c_h} "
				agg_cn += f"{c_n} "
				agg_cr += f"{c_r} "
				aggd += f"{c_d} "
			
			print_queue.extend([aggd, agg_ch, aggd, agg_cn, aggd, agg_cr, aggd])
			print_queue.append("")
			
		for ln in print_queue:
			print(ln)
		print()

		if update_mode == Nodule.UPDATE_ALL:
			input()

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
	
	def str_state(self):
		return "1" if self.state else "0"

class Conjunction(Nodule):

	def __init__(self, def_str: str) -> None:
		super().__init__(def_str)
		self.finalized = False
		self.incoming_connections = {}
		self.has_been_tripped = False
	
	def input(self, signal, last_name) -> None:
		if not self.finalized:
			raise ValueError(f"Conjunction {self.name} was not finalized")
		
		super().input(signal, last_name)
		self.incoming_connections[last_name] = signal
		out = not all(self.incoming_connections.values())

		if not out:
			self.has_been_tripped = True

		for target in self.targets:
			Nodule.PULSE_QUEUE.append((target, out, self.name))

	def finalize(self):
		for nodule in Nodule.REGISTRY.values():
			nodule: Nodule
			if self.name in nodule.targets:
				self.incoming_connections[nodule.name] = False
		self.finalized = True

	def str_state(self):
		my_str_state = ""
		sortkey = lambda n: Nodule.SORT_INDEX.get(n, -1)
		for inc in sorted(self.incoming_connections.keys(), key=sortkey):
			my_str_state += Nodule.REGISTRY[inc].str_state()
		return f"{my_str_state}"


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

	flipflops = []
	conjunctions = []
	for definition in lines:
		if definition[0] == "b":
			Broadcaster(definition)
		elif definition[0] == "%":
			flipflops.append(FlipFlip(definition))
		elif definition[0] == "&":
			conjunctions.append(Conjunction(definition))

	watch_list = {}
	for conj in conjunctions:
		conj.finalize()
		if conj.name in ("lx", "db", "qz", "sd"):
			watch_list[conj] = False
	
	presses = 0
	while not Nodule.FINISHED:
		Nodule.press_button_nodule(False)
		presses += 1

		for conj in watch_list:
			if not watch_list[conj] and conj.has_been_tripped:
				watch_list[conj] = presses
		if all(watch_list.values()):
			prod = 1
			for v in watch_list.values():
				prod *= v
			return prod
	
	raise LookupError("Somehow, this function finished without finding the answ"
				   	  "er. What's the heat death of the universe like?")

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