# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

import itertools

try:
	input_lines = io.read_input_as_lines(14)
	example_lines = io.read_example_as_lines(14)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]

def do_part_one_for(lines):
	init_map = algos.vector_map_from_string_list(lines, default_fn=lambda: "#")
	rock_positions = [v for v in init_map.keys() if init_map[v] == "O"]
	rock_positions = sorted(rock_positions, key=lambda x:x.y)
	up = vector.UP()
	rock_positions_settled = []
	for rp in rock_positions.copy():
		while init_map[rp + up] not in ("#", "O"):
			init_map[rp] = "."
			init_map[rp + up] = "O"
			rp += up
		rock_positions_settled.append(rp)
	
	algos.print_map(init_map)

	sum_load = 0
	max_load = len(lines)
	for settled in rock_positions_settled:
		sum_load += max_load - settled.y
	return sum_load

def calculate_load(rock_positions, max_y):
	return sum(max_y - r.y for r in rock_positions)


def do_a_spin_cycle(platform):
	rocks = [v for v in platform if platform[v] == "O"]

	MAX_Y = max([v.y for v in platform.keys()])
	MAX_X = max([v.x for v in platform.keys()])

	operations = [vector.UP(), vector.LEFT(), vector.DOWN(), vector.RIGHT()]
	sort_ops = [lambda v: v.y, lambda v: v.x, lambda v: MAX_Y - v.y, 
	     		lambda v: MAX_X - v.x]

	for op_ind, op in enumerate(operations):
		rocks = sorted(rocks, key=sort_ops[op_ind])
		for i in range(len(rocks)):
			while platform[rocks[i] + op] not in ("#", "O"):
				platform[rocks[i]] = "."
				rocks[i] += op
				platform[rocks[i]] = "O"

def do_part_two_for(lines):
	platform = algos.vector_map_from_string_list(lines, default_fn=lambda: "#")
	log = defaultdict(list)
	cycles_to_perform = 1000000000
	detecting_cycle = True
	while cycles_to_perform:
		# We will eventually reach a stable, cyclical pattern. When we detect 
		# said cycle, we can jump ahead.
		if detecting_cycle:
			# While we haven't found a cycle (and I recognize, we're using cycle
			# to mean two things here. I'm referring to a cycle of end locations
			# after performing the spin operation... a cycle of spin cycles... a
			# meta-cycle!)
			#
			# While we haven't found a metacycle, log the results after each 
			# spin cycle.
			hash_tup = tuple(v for v in platform.keys() if platform[v] == "O")
			log[hash_tup].append(1000000000 - cycles_to_perform)

			# If the results match a result we've seen before, then we're in a 
			# metacycle, so we can extrapolate where we'll end up after some 
			# number of repetitions of this metacycle:
			if len(log[hash_tup]) > 1:
				detecting_cycle = False
				period = log[hash_tup][1] - log[hash_tup][0]
				meta_cycles = cycles_to_perform // period
				cycles_to_perform -= meta_cycles * period

		do_a_spin_cycle(platform)
		cycles_to_perform -= 1

		# Debugging check-ins:
		if not (1000000000 - cycles_to_perform) % 100:
			pass
	
	rocks = tuple(v for v in platform.keys() if platform[v] == "O")
	return calculate_load(rocks, len(lines))

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"This is the prompt for Part One of the problem.\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe <THING THEY WANT> is {results}")
	print(f"\tWe expected: 136\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe <THING THEY WANT> is {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"This is the prompt for Part Two of the problem.\n")

	results = do_part_two_for(example_lines)
	print(f"When we do part two for the example input:")
	print(f"\tThe <THING THEY WANT> is {results}")
	print(f"\tWe expected: 64\n")
	
	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe <THING THEY WANT> is {results}\n")

def print_header():
	print("--- DAY 14: <TITLE GOES HERE> ---\n")
