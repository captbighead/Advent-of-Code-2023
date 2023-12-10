# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

try:
	input_lines = io.read_input_as_lines(9)
	example_lines = io.read_example_as_lines(9)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]

def extrapolate(sequence_def):
	sequence = [int(n) for n in sequence_def.split()]
	derivatives = [sequence]

	# Generate 'derivative' sequences. (Loosely basing the term off of what I 
	# remember from calculus)
	while sum(derivatives[-1]) != 0:
		derivatives.append([])
		for i in range(len(derivatives[-2])-1):
			derivatives[-1].append(derivatives[-2][i+1] - derivatives[-2][i])

	for d in range(-2, 0-len(derivatives)-1, -1):
		this_layer = derivatives[d]
		prev_layer = derivatives[d+1]
		derivatives[d].append(this_layer[-1] + prev_layer[-1])

	return sequence[-1]

def extrapolate_backwards(sequence_def):
	sequence = [int(n) for n in sequence_def.split()]
	derivatives = [sequence]

	# Generate 'derivative' sequences. (Loosely basing the term off of what I 
	# remember from calculus)
	while sum(derivatives[-1]) != 0:
		derivatives.append([])
		for i in range(len(derivatives[-2])-1):
			derivatives[-1].append(derivatives[-2][i+1] - derivatives[-2][i])

	for d in range(-2, 0-len(derivatives)-1, -1):
		this_layer = derivatives[d]
		prev_layer = derivatives[d+1]
		derivatives[d].insert(0, this_layer[0] - prev_layer[0])

	return sequence[0]


def do_part_one_for(lines):
	return sum(extrapolate(ln) for ln in lines)

def do_part_two_for(lines):
	return sum(extrapolate_backwards(ln) for ln in lines)

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"Given a series of increasing sequences, we need to determine the ne"
	   	  f"xt value in each sequence.\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe sum of the next values for each sequence is {results}")
	print(f"\tWe expected: 114\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe sum of the next values for each sequence is {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"Given a series of increasing sequences, we need to determine the pr"
	   	  f"ior value before the sequence began (IE: extrapolate backwards)\n")

	results = do_part_two_for(example_lines)
	print(f"When we do part two for the example input:")
	print(f"\tThe sum of the prior values for each seqence is {results}")
	print(f"\tWe expected: 2\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe sum of the prior values for each seqence is {results}\n")

def print_header():
	print("--- DAY 9: <TITLE GOES HERE> ---\n")
