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

def count_arrangements(spring_array):
	spring_string, checksums = spring_array.split()
	checksums = [int(n) for n in checksums.split(",")]
	regions = []
	new_reg = True
	for c in spring_string:
		# We are expecting a new region, but we've instead got whitespace
		if c == "." and new_reg:
			continue

		# We are expecting a new region, and we've found a piece of one:
		if c != "." and new_reg:
			new_reg = False
			regions.append(c)
			continue

		# We in a region. If we find whitespace, this region is done. 
		if c == ".":
			new_reg = True
			continue

		# We are in a region and we didn't find whitespace, so we add this to 
		# the region string. 
		regions[-1] += c

	print(f"--------------------\n\t The String: {spring_string}\n")
	print(f"\tI've identified {len(regions)} regions: ")
	for reg in regions:
		print(f"\t\t- {reg}")
	print()
	print(f"\tThere are {len(checksums)} final regions: {checksums}")
	print()

	return 0
		




def do_part_one_for(lines):
	summation = 0
	for line in lines:
		sequence, checksums = line.split()
		sequence = sequence.replace(".", "0").replace("#", "1")
		
		#print("SEQUENCE:")
		
		checksums = [n for n in checksums.split(",")]
		options = product("01", repeat=sequence.count("?"))

		re_str = "0*"
		for n in checksums:
			re_str += "1{" + str(n) + "}0+"
		re_str = re_str[:-1] + "*$"

		pattern = re.compile(re_str)

		count = 0
		for option in options: 
			seq_copy = sequence
			for i in range(len(option)):
				seq_copy = seq_copy.replace("?", option[i], 1)

			if pattern.match(seq_copy):
				#print(f"\t{seq_copy}")
				count += 1

		summation += count
		#print(f"TOTAL OPTIONS: {count}\n")

	return summation






	#return sum(count_arrangements(ln) for ln in lines)

def do_part_two_for(lines):
	pass

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
	print(f"\tThe <THING THEY WANT> is {results}\n")

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
