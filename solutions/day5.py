# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

try:
	input_lines = io.read_input_as_lines(5)
	example_lines = io.read_example_as_lines(5)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]

class almanac:

	def __init__(self, almanac_lines) -> None:
		seed_def = almanac_lines[0]
		self.seeds = [int(n) for n in seed_def.replace("seeds: ", "").split()]

		# Store the to, from states being transitioned in each functions, and 
		# then interpret the ranges.
		function_defs = []
		new_fn = True
		for line in almanac_lines[2:]:
			# First line after an empty newline (or first line in loop) inits fn
			if new_fn:
				new_fn = False
				line = line.replace(" map:", "")
				orig, dest = line.split("-to-")
				function_defs.append({"orig": orig, "dest": dest, "ranges":[]})
				continue
			
			# Empty line means our function is now done. Flag appropriately
			elif line == "":
				new_fn = True
				continue

			# Otherwise, we just store the range as ints
			range_vals = tuple([int(n) for n in line.split()])
			function_defs[-1]["ranges"].append(range_vals)
		
		# Map the current state to the function that transforms it into it's new
		# state and value
		self.lookup = {}
		for fdef in function_defs:
			self.lookup[fdef["orig"]] = self.genfn(fdef["dest"], fdef["ranges"])
		
	def genfn(self, new_state, ranges):
		# Formatting: Dest_Range_Start, Source_Range_Start, Range_Length
		def transform(n):
			new_n = n
			for dest_start, src_start, range_len in ranges:
				if n >= src_start and n < src_start + range_len:
					delta = n - src_start
					new_n = dest_start + delta
					break
			return (new_state, new_n)	# Defaults to identity if not in a range
		return transform

def do_part_one_for(lines):
	elfmanac = almanac(lines)
	best = 999999999999999999
	for val in elfmanac.seeds:
		state = "seed"
		while state != "location":
			state, val = elfmanac.lookup[state](val)
		best = min(best, val)
	return best

def do_part_two_for(lines):
	pass

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"Given a bizarre almanac as an input, what is the lowest location nu"
	   	  f"mber one of our starting seeds ends up in?\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe lowest location number is {results}")
	print(f"\tWe expected: 35\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe lowest location number is {results}\n")

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
	print("--- DAY 5: If You Give a Seed a Ferilizer ---\n")
