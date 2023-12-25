# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

try:
	input_lines = io.read_input_as_lines(21)
	example_lines = io.read_example_as_lines(21)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]

def do_part_one_for(lines, steps=64):
	grid_map = algos.vector_map_from_string_list(lines)
	orig = vector(len(lines) // 2, len(lines) // 2)
	tracked = set([orig])
	current = set([orig])
	rem_steps = steps
	while rem_steps:
		new_steps = set()
		for posn in current:
			for n in posn.adjacents:
				if n not in tracked and grid_map[n.congruent(len(lines))] != "#":
					new_steps.add(n)
					tracked.add(n)
		current = new_steps
		rem_steps -= 1

	return len([v for v in tracked if (v.x + v.y) % 2 == steps % 2])


def do_part_two_for(lines):
	DIM = len(lines)
	grid_map = algos.vector_map_from_string_list(lines, default_fn=lambda: "#")
	all_plots = len([v for v in grid_map if grid_map[v] != "#"])
	origin = vector(DIM // 2, DIM // 2)
	target_steps = 26501365
	tracked = {}

	# It takes 131 steps to get from the center point to all the other center 
	# points, and coincidentally, that's how long it takes for the first square
	# to be entirely accessible (for the actual input). 

	# This means that from every furthest point after 131 steps, it's 

	# Figure out how long it takes to get to any space from the center. 
	steps = 0
	recent_steps = set([origin])
	breakout = False
	while len(tracked) != all_plots and recent_steps and not breakout:
		steps += 1
		next_steps = set()
		for v in recent_steps:
			for adj in v.adjacents:
				if adj not in grid_map:
					continue
				if adj not in tracked and grid_map[adj.congruent(DIM)] != "#":
					next_steps.add(adj)
					tracked[adj] = steps

		breakout = all([(u * 131) + origin in tracked for u in vector.UNIT_VECTORS()])
		recent_steps = next_steps

	print()
	


def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"This is the prompt for Part One of the problem.\n")

	print(f"When we do part one for the example input:")
	results = do_part_one_for(example_lines, 6)
	print(f"\tThe number of reachable plots is {results}")
	print(f"\tWe expected: 16\n")


	print(f"When we do part one for the example input:")
	results = do_part_one_for(input_lines, 65)
	print(f"\tThe number of reachable plots is {results}")
	print(f"\tWe expected: \n")


	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe number of reachable plots is {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"This is the prompt for Part Two of the problem.\n")

	#print(f"When we do part two for the example input:\n")
	#tests = [(6, 16), (10, 50), (50, 1594), (100, 6536), (500, 167004), 
	#  		 (1000, 668697), (5000, 16733044)]
	#for steps, expected in tests:
	#	results = do_part_two_for(example_lines, steps)
	#	print(f"\tThe number of reachable plots after {steps} steps is "
	#		  f"{results}")
	#	print(f"\tWe expected: {expected}\n")

	print(f"When we do part two for the actual input:")
	results = do_part_two_for(input_lines)
	print(f"\tThe number of reachable plots is {results}\n")

def print_header():
	print("--- DAY 21: <TITLE GOES HERE> ---\n")
