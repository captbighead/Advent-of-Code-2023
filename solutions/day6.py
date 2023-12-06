# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

try:
	input_lines = io.read_input_as_lines(6)
	example_lines = io.read_example_as_lines(6)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]

def do_part_one_for(lines):
	times = [int(n) for n in lines[0].replace("Time:", "").split()]
	dists = [int(n) for n in lines[1].replace("Distance:", "").split()]

	product = 1
	for race_num in range(len(times)):
		T = times[race_num]
		D = dists[race_num]
		options = 0
		for t in range(T+1):
			charge = t
			travel = T - t
			d = charge * travel
			options += 1 if d > D else 0
		product *= options
	return product

def do_part_two_for(lines):
	lines = [ln.replace(" ", "") for ln in lines]
	TIME = int(lines[0].replace("Time:", ""))
	DIST = int(lines[1].replace("Distance:", ""))
	options = TIME + 1

	# count up from 0 until we're winning. 
	t = 0
	while t * (TIME - t) < DIST:
		options -= 1
		t += 1

	# count down from TIME until we're winning. 
	t = TIME
	while t * (TIME - t) < DIST:
		options -= 1
		t -= 1

	# ... That's our range. 
	#
	# ... there are smarter ways to do it... but... like... why?
	return options


def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"Ummm... we hold down button, boat go fast?\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe product of the different ways you can win each race is "
		  f"{results}")
	print(f"\tWe expected: 288\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe product of the different ways you can win each race is "
		  f"{results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"But wait... this is also absurd... right?\n")

	results = do_part_two_for(example_lines)
	print(f"When we do part two for the example input:")
	print(f"\tThe same product thing from before but for a bigger number is "
		  f"{results}")
	print(f"\tWe expected: 71503\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe same product thing from before but for a bigger number is "
		  f"{results}\n")

def print_header():
	print("--- DAY 6: Wait For It ---\n")
