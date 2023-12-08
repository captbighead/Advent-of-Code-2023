# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

try:
	input_lines = io.read_input_as_lines(8)
	example_lines = io.read_example_as_lines(8)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]

example_lines_p2 = [
	"LR", 
	"", 
	"11A = (11B, XXX)", 
	"11B = (XXX, 11Z)", 
	"11Z = (11B, XXX)", 
	"22A = (22B, XXX)", 
	"22B = (22C, 22C)", 
	"22C = (22Z, 22Z)", 
	"22Z = (22B, 22B)", 
	"XXX = (XXX, XXX)"
]

def do_part_one_for(lines):
	instructions = lines[0]
	node_list = lines[2:]
	graph = {}
	for n_def in node_list:
		k, l, r = algos.erase(n_def, ["= (", ",", ")" ]).split()
		graph[k] = {"L": l, "R": r}
	current = "AAA"
	inst_ind = 0
	steps = 0
	while current != "ZZZ":
		c = instructions[inst_ind]
		inst_ind = (inst_ind + 1) % len(instructions)
		steps += 1
		current = graph[current][c]
	return steps

def do_part_two_for(lines):
	instructions = lines[0]
	node_list = lines[2:]
	a_node_trace = []
	a_nodes = []
	graph = {}
	for n_def in node_list:
		k, l, r = algos.erase(n_def, ["= (", ",", ")" ]).split()
		if k.endswith("A"):
			a_nodes.append(k)
			a_node_trace.append(k)
		graph[k] = {"L": l, "R": r}

	steps = 0
	inst_ind = 0
	i_periods = [0] * len(a_nodes)
	while True:
		# Grab the current instruction for this tick: 
		inst = instructions[inst_ind]
		inst_ind = (inst_ind + 1) % len(instructions)
		steps += 1

		synced = True
		for i, node in enumerate(a_nodes.copy()):
			a_nodes[i] = graph[node][inst]
			synced = synced and a_nodes[i].endswith("Z")

			if a_nodes[i].endswith("Z"):
				i_periods[i] = steps

				if len([n for n in i_periods if n]) == len(a_nodes):
					prime_factors = defaultdict(int)
					for ind_n, n in enumerate(i_periods):
						print(f"\tThe period of the path travelled at {ind_n} i"
							  f"s {n}")
						n_prime_factors = algos.prime_factorize(n)
						for b, e in n_prime_factors:
							prime_factors[b] = max(prime_factors[b], e)
						
					LCM = 1
					for f in prime_factors.keys():
						LCM *= f ** prime_factors[f]

					print()
					print(f"The Least Common Multiple is: {LCM}")
					return LCM

				#something_to_show = True
				#a_node_trace[i] += f" -> {a_nodes[i]} at {steps}"

		#	a_node_trace[i] += f" -> {a_nodes[i]}"
		
		if synced:
			return steps
		
		#elif something_to_show and steps % 100 == 0:
		#	something_to_show = False
		#	print("Aha. There was trickery! Let's look at some traces:")
		#	for trace in a_node_trace:
		#		print(f"\t{trace}")
		#	input()
			
	



def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"This is the prompt for Part One of the problem.\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe number of steps it takes to reach ZZZ following the instructi"
		  f"ons is {results}")
	print(f"\tWe expected: 6\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe number of steps it takes to reach ZZZ following the instructi"
		  f"ons is {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"Now we need to simultaneously leave from every __A node at once and"
	   	  f" only stop when we end up at entirely __Z nodes.\n")

	results = do_part_two_for(example_lines_p2)
	print(f"When we do part two for the example input:")
	print(f"\tThe number of steps until all ghosts have arrived at a __Z node s"
		  f"imultaneously is {results}")
	print(f"\tWe expected: 6\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe number of steps until all ghosts have arrived at a __Z node s"
		  f"imultaneously is {results}\n")

def print_header():
	print("--- DAY 8: Haunted Wasteland ---\n")
