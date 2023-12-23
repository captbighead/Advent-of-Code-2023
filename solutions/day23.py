# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

try:
	input_lines = io.read_input_as_lines(23)
	example_lines = io.read_example_as_lines(23)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]

def do_part_one_for(lines):
	grid_map = algos.vector_map_from_string_list(lines, default_fn=lambda: "#")
	orig = vector(1, 0)
	DEST = vector(len(lines[0]) - 2, len(lines) - 1)
	LEGAL_STEPS = {
		".": vector.UNIT_VECTORS(), 
		"<": [vector.LEFT()], 
		">": [vector.RIGHT()], 
		"^": [vector.UP()], 
		"v": [vector.DOWN()]
	}

	search_stack = [(orig, [vector.DOWN()], 0, set())]
	visited = set()

	def get_options(current):
		options = []
		for opt in LEGAL_STEPS[grid_map[current]]:
			step = current + opt
			tile = grid_map[step]
			is_backtrack = step in visited
			is_wall = tile == "#"
			is_slope = not is_wall and len(LEGAL_STEPS[tile]) == 1
			is_unclimable = is_slope and LEGAL_STEPS[tile][0] != opt
			if not is_backtrack and not is_wall and not is_unclimable:
				options.append(opt)
		return options

	best = 0
	visited = set()
	while search_stack:
		current, options, path_len, visited = search_stack.pop()
		visited.add(current)

		# If we hit the end, mark it, and then backtrack
		if current == DEST:
			best = max(best, path_len)
			continue

		# If there are no options here, we backtrack.
		if not options:
			continue

		# Otherwise, we remove the option we're checking from the options we'll
		# visit if we backtrack, and pop it back on the search_stack
		next = current + options.pop()
		search_stack.append((current, options, path_len, visited.copy()))
		visited.add(next)
		current = next
		path_len += 1

		# Follow until another branch: 
		new_options = get_options(current)
		while len(new_options) == 1:
			current += new_options[0]
			new_options = get_options(current)
			visited.add(current)
			path_len += 1
		
		search_stack.append((current, new_options, path_len, visited.copy()))
	return best



def do_part_two_for(lines):
	new_lines = []
	for ln in lines:
		for slope in "><v^":
			ln = ln.replace(slope, ".")
		new_lines.append(ln)
	return do_part_one_for(new_lines)

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"This is the prompt for Part One of the problem.\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe longest path possible without repeats is {results}")
	print(f"\tWe expected: 94\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe longest path possible without repeats is is {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"Do it again, but without slopes!\n")

	results = do_part_two_for(example_lines)
	print(f"When we do part two for the example input:")
	print(f"\tThe longest path is {results}")
	print(f"\tWe expected: 154\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe longest path is {results}\n")

def print_header():
	print("--- DAY 23: A Long Walk ---\n")
