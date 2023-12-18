# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

from itertools import product
import re

try:
	input_lines = io.read_input_as_lines(12)
	example_lines = io.read_example_as_lines(12)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]

def count_arrangements(array, counts, pattern):

	# Base case, we've inserted all of the broken segments. Turn any remaining
	# unknowns into fixed springs and check against the pattern:
	if len(counts) == 0:
		return 1 if pattern.match(array.replace("?", ".")) else 0
	
	# Otherwise, try inserting our next set of broken springs: 
	arrangements = 0
	insert_val = counts[0]
	next_vals = counts[1:] if len(counts) > 0 else []
	insert_options = [i for i in range(len(array)) if array[i] == "?"]
	min_spaces_for_next = sum(next_vals)
	insert_options = insert_options[:len(insert_options) - min_spaces_for_next]
	for opt in insert_options:

		# Don't try to insert it into a space that's too small for it.
		if array[opt:opt + insert_val] == "?" * insert_val:
			prefix = array[:opt].replace("?", ".")
			inserted = "#" * insert_val
			suffix = array[opt + insert_val:]	
			var_array = prefix + inserted + suffix
			arrangements += count_arrangements(var_array, next_vals, pattern)
	
	return arrangements


def do_part_one_for(lines):
	summation = 0
	for line in lines:
		sequence, counts = line.split()
		counts = [int(n) for n in counts.split(",")]

		# Prune leading known characters
		while sequence[0] in (".", "#"):
			if sequence[0] == "#":
				counts[0] -= 1
				if counts[0] == 0:
					counts.pop(0)
			sequence = sequence[1:]

		# Prune trailing known characters
		while sequence[-1] in (".", "#"):
			if sequence[-1] == "#":
				counts[-1] -= 1
				if counts[-1] == 0:
					counts.pop()
			sequence = sequence[:-1]

		# Build a pattern off of what's left.
		patt_str = "\.*"
		for c in counts:
			patt_str += "#{" + str(c) + "}\.+"
		patt_str = patt_str[:-1] + "*$"
		pattern = re.compile(patt_str)

		summation += count_arrangements(sequence, counts, pattern)

	return summation

def do_part_two_for(lines):
	summation = 0
	return summation

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"Given the following arrays of broken springs and their descriptors,"
	   	  f" we need to find the number of arrangements of undamaged/damaged sp"
		  f"rings that are possible.\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe sum of the number of arrangements is {results}")
	print(f"\tWe expected: 21\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe The sum of the number of arrangements is {results}\n")

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
	print("--- DAY 12: <TITLE GOES HERE> ---\n")
