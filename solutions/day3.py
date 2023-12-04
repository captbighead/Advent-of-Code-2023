# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

try:
	input_lines = io.read_input_as_lines(3)
	example_lines = io.read_example_as_lines(3)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]

def is_symbol(c):
	return c != "." and not c.isnumeric()

def parse_schematic(schematic_lines):
	# Parse the original map as the characters at each position. Then iterate 
	# over the symbols, and map those symbols to their part numbers. 
	orig = algos.vector_map_from_string_list(schematic_lines)
	result = {}

	# Bind references to directions so we can search along them.
	LEFT = vector.LEFT()
	RIGHT = vector.RIGHT()

	# Systematically check each postion around each symbol. It's very likely 
	# we'll run into numbers around one symbol that we already parsed from 
	# checking around a different, earlier symbol, so remember the coordinates
	# of digits that have been processed. 
	symbol_positions = [v for v in orig.keys() if is_symbol(orig[v])]
	checked = set([])

	for part_xy in symbol_positions:
		result[(part_xy, orig[part_xy])] = []
		for adj in part_xy.surrounding:
			# If we get past this continue, we are a numeric string that hasn't
			# been a part of a previous numeric string. 
			if not orig[adj].isnumeric() or adj in checked:
				continue
			checked.add(adj)

			# Compose the string from consecutive digits to the left/right
			num_str = orig[adj]
			ladj, radj = adj + LEFT, adj + RIGHT
			while orig[ladj] != "." and orig[ladj].isnumeric():
				num_str = orig[ladj] + num_str
				checked.add(ladj)	# Don't try again from this spot later ;)
				ladj += LEFT
			while orig[radj] != "." and orig[radj].isnumeric():
				num_str = num_str + orig[radj]
				checked.add(radj)
				radj += RIGHT

			result[(part_xy, orig[part_xy])].append(int(num_str))
	
	return result


def do_part_one_for(lines):
	part_lookup = parse_schematic(lines)
	return sum(sum(v) for v in part_lookup.values())

def do_part_two_for(lines):
	gear_ratio_sum = 0
	parts = parse_schematic(lines)
	for coord, part in parts.keys():
		if part == "*" and len(parts[coord, part]) == 2:
			gear_ratio_sum += parts[coord, part][0] * parts[coord, part][1]
	return gear_ratio_sum


def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"We've been given an engine schematic for a gondola, consisting of s"
	   	  f"ymbols with part numbers labelling them, and other numbers we don't"
		  f" understand yet. Given that part numbers are adjacent to a symbol ("
		  f"even diagonally), what is the sum of all of the part numbers in our"
		  f" schematic?\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe sum of the part numbers is {results}")
	print(f"\tWe expected: 4361\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe sum of the part numbers is {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"For Part Two, we're adding the 'gear ratios' of the gear parts toge"
	   	  f"ther. Gears are asterisk symbols with exactly two part numbers next"
		  f" to them, and their gear ratio is the product of those numbers.\n")

	results = do_part_two_for(example_lines)
	print(f"When we do part two for the example input:")
	print(f"\tThe sum of the gear ratios is {results}")
	print(f"\tWe expected: 467835\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe sum of the gear ratios is {results}\n")

def print_header():
	print("--- DAY 3: Gear Ratios ---\n")
