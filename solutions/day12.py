# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

from functools import lru_cache

try:
	input_lines = io.read_input_as_lines(12)
	example_lines = io.read_example_as_lines(12)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]

@lru_cache
def arrangements(array, counts):
	# Base Cases: there are no more counts, or there are no more springs:

	# We've run out of counts to apply; if there are no more broken springs left
	# in the array then this was valid, otherwise it was not.  
	if not counts:
		return 1 if not array.count("#") else 0
	
	# We still have counts but no more string left. 
	if not array:
		return 0	

	# Otherwise recurse some more!
	results = 0

	# If the next space is a fixed spring or an unknown we can try to turn into
	# a fixed spring, that's one possibility, multiplied by all its subsequent 
	# other possibilities.
	if array[0] in ".?":
		results += arrangements(array[1:], counts)
	
	# If the next space is a broken spring or an unknown we can try to turn into
	# a broken spring, try and stick the whole next contiguous section in. If it
	# couldn't be fit in, that's fine. 
	if array[0] in "#?":
		to_replace = array[:counts[0]]
		fits = len(array) >= counts[0]
		fits = fits and (len(array) == counts[0] or array[counts[0]] != "#")
		fits = fits and "." not in to_replace
		if fits:
			results += arrangements(array[counts[0] + 1:], counts[1:])
	
	return results

def do_part_one_for(lines):
	summation = 0
	for ln in lines:
		array, count_str = ln.split()
		counts = tuple(int(n) for n in count_str.split(","))
		arrs = arrangements(array, counts)
		summation += arrs

		# Print out the arrangements if it's the example case.
		if len(lines) < 10:
			print(f"\t{arrs} arrangements for {array} {counts}")

	# If we just did the example case then we want a spacer before we return.
	if len(lines) < 10:
		print()

	return summation

def do_part_two_for(lines):
	summation = 0
	for ln in lines:
		array, count_str = ln.split()
		counts = tuple(int(n) for n in count_str.split(","))
		counts *= 5
		array += ("?" + array) * 4
		arrs = arrangements(array, counts)
		summation += arrs

		if len(lines) < 10:
			print(f"\t{arrs} arrangements for {array} {counts}")
	if len(lines) < 10:
		print()
	return summation

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"Given lists of fixed and broken springs with some unknown values, w"
       	  f"hat is the sum of valid arrangements of fixed/broken springs that c"
		  f"an be substituted for the unknowns?\n")

	print(f"When we do part one for the example input:\n")
	results = do_part_one_for(example_lines)
	print(f"\tThe number of arrangements of fixed and broken springs is "
		  f"{results}")
	print(f"\tWe expected: 21\n")

	print(f"When we do part one for the actual input:")
	results = do_part_one_for(input_lines)
	print(f"\tThe number of arrangements of fixed and broken springs is "
		  f"{results}\n")
	print(f"\tWe expected: 7506 (we've submitted and verified part one)\n")


def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"When the lists are 'unfolded' (IE: concatenated to themselves five "
       	  f"times), how many arrangements are there?\n")

	print(f"When we do part two for the example input:")
	results = do_part_two_for(example_lines)
	print(f"\tThe number of arrangements for the unfolded array is {results}")
	print(f"\tWe expected: 525152\n")

	print(f"When we do part two for the actual input:")
	results = do_part_two_for(input_lines)
	print(f"\tThe number of arrangements for the unfolded array is {results}\n")

def print_header():
	print("--- DAY 12: Hot Springs ---\n")
