# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

from itertools import product

try:
	input_lines = io.read_input_as_lines(21)
	example_lines = io.read_example_as_lines(21)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]

def do_part_one_for(lines, steps=64):
	gridmap = algos.vector_map_from_string_list(lines)
	orig = vector(len(lines) // 2, len(lines) // 2)
	tracked = set([orig])
	current = set([orig])
	rem_steps = steps
	while rem_steps:
		new_steps = set()
		for posn in current:
			for n in posn.adjacents:
				if n not in tracked and gridmap[n.congruent(len(lines))] != "#":
					new_steps.add(n)
					tracked.add(n)
		current = new_steps
		rem_steps -= 1

	return len([v for v in tracked if (v.x + v.y) % 2 == steps % 2])


def do_part_two_for(lines, target_steps=26501365):
	DIM = len(lines)
	grid_map = algos.vector_map_from_string_list(lines)
	origin = vector(DIM // 2, DIM // 2)
	tracked = {}

	# We 'BFS' until we reach a periodic state that we can extrapolate from
	dist = 2 * DIM + DIM // 2

	extrapolation_target = [origin + (u * dist) for u in vector.UNIT_VECTORS()]
	target_steps -= dist
	exSteps = target_steps // DIM

	# The 'BFS': Keep track of the leading edge and then step out from it and 
	# record the minimum distance it took to get to each space we step to.
	steps = 0
	recent_steps = set([origin])
	while not all([t in tracked for t in extrapolation_target]):
		steps += 1
		next_steps = set()
		for v in recent_steps:
			for adj in v.adjacents:
				if adj not in tracked and grid_map[adj.congruent(DIM)] != "#":
					next_steps.add(adj)
					tracked[adj] = steps
		recent_steps = next_steps

	# From here on out, the graph grows by a number of repeats of regions we've
	# already defined:
	#
	#  	State: O		State: O + 1		State: O + 2
	#		
	#	. a N b .		. . a N b . .		. . . a N b . . .
	#	a A F B b		. a A F B b .		. . a A F B b . .
	#	W F F F E	->	a A F F F B b	->	. a A F F F B b .
	#	c C F D d		W F F F F F E		a A F F F F F B b
	#	. c S d .		c C F F F B b		W F F F F F F F E
	#					. c C F B b .		c C F F F F F D d
	#					. . c S b . .		. c C F F F D d .
	#										. . c C F D d . .
	#										. . . c S d . . .
	#						
	#	abcd - 2		abcd - 3			abcd - 4
	#	ABCD - 1		ABCD - 2			ABCD - 3
	#	NESW - 1		NESW - 1			NESW - 1
	#	F - 5			F - 13				F - 25

	region_lookup = {}
	for rx, ry in product(range(-2, 3), repeat=2):
		r_vec = vector(rx, ry)
		r_offset = r_vec * DIM
		region_lookup[r_vec] = [0, 0]	# Count reachable plots by step parity
		for x, y in product(range(DIM), repeat=2):
			v = vector(x, y) + r_offset
			plot_steps = tracked.get(v, -1)
			if plot_steps != -1:
				region_lookup[r_vec][plot_steps % 2] += 1

	# From our map we pull out single instances of each type of region we are 
	# going to use. 
	abcd_ext = []
	abcd_int = []
	nesw = []
	full = vector()
	for r_key in region_lookup.keys():
		mxabs = max(abs(r_key.x), abs(r_key.y))
		mnabs = min(abs(r_key.x), abs(r_key.y))
		reg_class = (mxabs, mnabs)
		if reg_class == (2, 1) and abs(r_key.x) == 2:
			abcd_ext.append(r_key)
		elif reg_class == (2, 0):
			nesw.append(r_key)
		elif reg_class == (1, 1):
			abcd_int.append(r_key)

	# Every region in the final construct is a carbon copy of a regions as 
	# it appears now, so the number of steps reachable in a region of our 
	# current structure have odd parity, and so they have odd parity in that 
	# corresponding copy of that same region in the final map... 
	abcd_evens = sum((exSteps + 2) * region_lookup[v][1] for v in abcd_ext)
	abcd_odds = sum((exSteps + 1) * region_lookup[v][1] for v in abcd_int)
	nesw_odds = sum(region_lookup[v][1] for v in nesw)
	
	# EXCEPT for the fact that the fully-accessible regions swap parity when you
	# transfer between them. To account for that we use our understanding of the
	# squared sequence we're doing to add copies of both. 
	full_evens = ((exSteps + 2) ** 2) * region_lookup[full][0]
	full_odds = ((exSteps + 1) ** 2) * region_lookup[full][1]

	return sum([full_evens, full_odds, abcd_odds, abcd_evens, nesw_odds])

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"This is the prompt for Part One of the problem.\n")

	print(f"When we do part one for the example input:")
	results = do_part_one_for(example_lines, 6)
	print(f"\tThe number of reachable plots is {results}")
	print(f"\tWe expected: 16\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe number of reachable plots is {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"This is the prompt for Part Two of the problem.\n")

	print(f"When we do part two for an arbitrary example I made up (the example"
       	  f" in this problem is so bad!), we use the the actual input but only "
		  f"go 589 steps (as opposed to the requested 26501365):")
	results = do_part_two_for(input_lines, 589)
	print(f"\tThe number of reachable plots is {results}")
	print(f"\tWe expected: 307031 (because I brute forced it)\n")

	print(f"When we do part two for the actual input:")
	results = do_part_two_for(input_lines)
	print(f"\tThe number of reachable plots is {results}\n")

def print_header():
	print("--- DAY 21: <TITLE GOES HERE> ---\n")
