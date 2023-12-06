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

	def __repr__(self) -> str:
		return f"[{self.rmin}, {self.rmax}]"

def generate_transform_function(dest, ranges):
	# Sort the (range, offset) tuples in ascending order of range so that we can
	# then fill in the gaps with their unrepresented ranges and their offset: 0
	ranges = sorted(ranges, key=lambda tup: tup[0].rmin)

	# Special insertion case when 0 is not the absolute minimum across ranges 
	if ranges[0][0].rmin != 0:
		old_abs_min = ranges[0][0].rmin
		ranges.insert(0, (inclusive_range(0, old_abs_min - 1), 0))

	# Now we iterate upwards, finding and filling all gaps with ranges that have
	# an offset of 0. 
	idx = 2		# Skip the first two, we know they're good. 
	while idx < len(ranges):
		range_prv, offset_prv = ranges[idx-1]
		range_idx, offset_idx = ranges[idx]
		if range_prv.rmax != range_idx.rmin - 1:
			midrange = inclusive_range(range_prv.rmax + 1, range_idx.rmin - 1)
			ranges.insert(idx, (midrange, 0))
			idx += 2
		else:
			idx += 1

	# At this point, 'ranges' is a comprehensive list of ranges with the offests
	# that get applied to numbers in those ranges. The transform function merely
	# subdivides out any input ranges into the ranges that would be generated if
	# put into the output ranges. 
	out_ranges = ranges

	def transform(range_list):
		transformed_ranges = []
		for in_range in range_list:
			start_idx = 0
			while (start_idx < len(out_ranges) and 
				   in_range.rmin > out_ranges[start_idx][0].rmax):
				start_idx += 1
			
			# If we've gone beyond the end of the out_range list, then the 
			# offset is 0 for the entire in_range, so we just return it as-is
			if start_idx >= len(out_ranges):
				transformed_ranges.append(in_range)
				continue

			#Otherwise, start translating ranges. 
			# r_range == "Remaining Range". AKA: The remaining part of the input
			# range to transform.
			r_range = in_range
			idx = start_idx
			while r_range != None and idx < len(out_ranges):
				# t_range == "Transformer Range": the range that transforms.
				t_range, offset = out_ranges[idx]

				# Easiest case: r_range is a subset of the transformer range
				if r_range.rmax <= t_range.rmax:
					new_range = inclusive_range(r_range.rmin + offset, 
								 				r_range.rmax + offset)
					transformed_ranges.append(new_range)
					r_range = None

				# Otherwise, we know r_range.rmin is within t_range, so we need
				# to transform the portion of r_range within t_range, and then
				# shuffle the remainder of r_range to the next iteration. 
				else: 
					new_range = inclusive_range(r_range.rmin + offset, 
								 				t_range.rmax + offset)
					transformed_ranges.append(new_range)
					r_range = inclusive_range(t_range.rmax + 1, r_range.rmax)
					idx += 1
			
			# If any of the range is left over, it's above the end of the 
			# function's range limit, so it gets an offset of 0 (IE: just add it
			# to the list of transformed ranges)
			if r_range != None:
				transformed_ranges.append(r_range)
		
		return (dest, transformed_ranges)
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
	transform_fns = {}
	working_fn_data = {}

	# Function definition happens when an empty line is encountered, but the 
	# input functions strip trailing empty lines, so the final function won't be
	# defined unless we append this empty string (or copy code)
	defs.append("")				

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
			transform_fns[orig] = generate_transform_function(dest, rngs)
			continue
		
		# Otherwise, just record the range:
		dstart, sstart, rlen =  [int(n) for n in def_ln.split()]
		range_val = inclusive_range(sstart, sstart + rlen - 1)
		offset = dstart - sstart
		working_fn_data["rngs"].append((range_val, offset))
	
	# At this point, transform_fns takes a list of ranges and then transforms it
	# into a different list of ranges based on the given states. 
	curr_ranges = seed_ranges
	curr_state = "seed"
	while curr_state != "location":
		curr_state, curr_ranges = transform_fns[curr_state](curr_ranges)
	curr_ranges = sorted(curr_ranges, key=lambda rng: rng.rmin)
	return curr_ranges[0].rmin




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
