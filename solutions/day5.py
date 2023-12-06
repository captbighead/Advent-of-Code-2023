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

class part_one_almanac:

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
	elfmanac = part_one_almanac(lines)
	best = 999999999999999999
	for val in elfmanac.seeds:
		state = "seed"
		while state != "location":
			state, val = elfmanac.lookup[state](val)
		best = min(best, val)
	return best

class inclusive_range:

	def __init__(self, rmin, rmax) -> None:
		self.rmin = rmin
		self.rmax = rmax

def generate_transform_function(dest, ranges):
	# Sort the (range, offset) tuples in ascending order of range so that we can
	# then fill in the gaps with their unrepresented ranges and their offset: 0
	ranges = sorted(ranges, key=lambda tup: tup[0])
	abs_max = max(ranges, key=lambda tup: tup[0].rmax)

	# Special insertion cases when 0 is not the absolute minimum across all 
	# ranges and abs_max is not the absolute max across all ranges
	if ranges[0][0].rmin != 0:
		old_abs_min = ranges[0][0].rmin
		ranges.insert(0, (inclusive_range(0, old_abs_min - 1), 0))
	if ranges[-1][0].rmax < abs_max:
		old_abs_max = ranges[-1][0].rmax
		ranges.append((inclusive_range(old_abs_max + 1, abs_max), 0))

	# Now we iterate upwards, finding and filling all gaps
	idx = 0
	while False:
		pass


	def transform(range_list):
		# TODO: Actually write this guy
		return dest, range_list
	return transform

def do_part_two_for(defs):
	# If we created range objects that could handle being split into 
	# multiple objects, then a range of seeds being checked against the 
	# seed-to-soil map would become a set of ranges of soils. We could then
	# process a set of ranges of soils to get a set of ranges of fertilizer,
	# etc...
	seed_range_defs = defs[0][7:].split()
	seed_ranges = []
	for i in range(len(seed_range_defs)// 2):
		rmin, rlen = int(seed_range_defs[i*2]), int(seed_range_defs[i*2+1])
		rmax = rmin + rlen - 1
		seed_ranges.append(inclusive_range(rmin, rmax))
	seed_ranges = sorted(seed_ranges, key=lambda r: r.rmin)
	
	new_fn = True
	transform_functions = {}
	working_fn_data = {}
	for def_ln in defs[2:]:
		# Are we starting a new function? 
		if new_fn:
			new_fn = False
			orig, dest = def_ln[:-5].split("-to-")
			working_fn_data["orig"] = orig
			working_fn_data["dest"] = dest
			working_fn_data["rngs"] = []
			continue

		# Are we *finalizing* the working function?
		elif def_ln == "":
			new_fn = True
			orig = working_fn_data["orig"]
			dest = working_fn_data["dest"]
			rngs = working_fn_data["rngs"]
			transform_functions[orig] = generate_transform_function(dest, rngs)
			continue
		
		# Otherwise, just record the range:
		dstart, sstart, rlen =  [int(n) for n in def_ln.split()]
		range_val = inclusive_range(sstart, sstart + rlen - 1)
		offset = dstart - sstart
		rngs.append((range_val, offset))




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
	print(f"PART TWO\n--------\n")
	print(f"The inital seed values given were a ruse! They're actually ranges i"
	   	  f"n and of themselves (and their ranges are absurdly large, too large"
		  f" to iterate over). What's the lowest location number *now*?\n")

	results = do_part_two_for(example_lines)
	print(f"When we do part two for the example input:")
	print(f"\tThe actual lowest location number is {results}")
	print(f"\tWe expected: 46\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe actual lowest location number is {results}\n")

def print_header():
	print("--- DAY 5: If You Give a Seed a Ferilizer ---\n")
