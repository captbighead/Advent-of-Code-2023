# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

import heapq

try:
	input_lines = io.read_input_as_lines(17)
	example_lines = io.read_example_as_lines(17)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]		


def do_part_one_for(lines):
	WORST_CASE = sum(int(n) for n in "".join(lines))
	default = lambda: WORST_CASE
	grid = algos.vector_map_from_string_list(lines, default, int)
	orig = vector()
	goal = max(grid.keys(), key=lambda v: orig.distance(v))

	# Can't do dijkstra's because the path with the best cost might not be legal
	best = WORST_CASE
	def recursive_dfs(position, heat_loss, path_set, last_three_set):
		nonlocal WORST_CASE, grid, goal, best

		if len(pre_path) == 999:
			print("Stack Overflow Reached")

		# Best case scenario would be a straight shot to the goal, where we only
		# lose one heat per step. If that would result in a worse heat loss than
		# our best discovered path so far, then this branch is dead. 
		if heat_loss + position.distance(goal) >= best:
			return
		
		if position == goal:
			best = min(best, heat_loss)
			return

		path_set = path_set.copy()
		last_move = position - last_three_set[-1] if len(last_three_set) else None
		last_three_set.append(position)

		options = vector.UNIT_VECTORS()
		# We can't go backwards
		if last_move != None:
			options.remove(last_move * -1)
		
		# If we haven't gone anywhere yet, we can't go left or right
		else:
			options.remove(vector.UP())
			options.remove(vector.LEFT())

		# If we've been to at least 3 destinations, we can't go in the same 
		# direction for a fourth time in a row. 
		last_three = None
		if len(path) > 3:
			last_three = set([path[i] - path[i-1] for i in range(-1, -4, -1)])
			if len(last_three) == 1:
				options.remove(last_move)

		options = sorted(options, key=lambda v: grid[position + v])

		# Now we speculate on pursuing the legal options: 
		for opt in options: 

			# In either of the following scenarios, we will never get back 
			# without crossing our tail. 
			if position.x == goal.x and opt == vector.UP():
				continue
			elif position.y == goal.y and opt == vector.LEFT():
				continue

			spec_pos = position + opt
			spec_heat = heat_loss + grid[spec_pos]
			if spec_heat < best and spec_pos not in path:
				recursive_dfs(spec_pos, spec_heat, path)
	recursive_dfs(orig, 0, [])
	return best




			


def do_part_two_for(lines):
	pass

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"Shortest path through grid where you can't go backwards, only left,"
	   	  f" right or forwards, and you can only go 3 steps forward before a tu"
		  f"rn.\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe least possible heat loss is {results}")
	print(f"\tWe expected: 102\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe least possible heat loss is {results}\n")

def solve_p2():
	return
	print(f"PART TWO\n--------\n")
	print(f"This is the prompt for Part Two of the problem.\n")

	results = do_part_two_for(example_lines)
	print(f"When we do part two for the example input:")
	print(f"\tThe <THING THEY WANT> is {results}")
	print(f"\tWe expected: <SOLUTION THEY WANT>\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe <THING THEY WANT> is {results}\n")

def print_header():
	print("--- DAY 17: Clumsy Crucible ---\n")
