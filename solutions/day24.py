# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

try:
	input_lines = io.read_input_as_lines(24)
	example_lines = io.read_example_as_lines(24)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]

def do_part_one_for(line_defs, is_example):
	MIN = 200000000000000 if not is_example else 7
	MAX = 400000000000000 if not is_example else 27

	def in_bounds(v):
		return v[0] >= MIN and v[0] <= MAX and v[1] >= MIN and v[1] <= MAX

	def generate_is_approaching_closure(x, y, m):
		# Assume P = (x, y) is on a line with slope m. This function returns a 
		# closure that takes a point v and returns true if that point is further
		# along the line from (x, y) (IE: v + nm = P, is n positive?)
		mx, my = m
		def is_approaching(v):
			vx, vy = v
			return vx < x if mx < 0 else vx > x and vy < y if my < 0 else vy > y
		return is_approaching

	lines = []
	approach_closures = []
	for line_def in line_defs:
		p, v = line_def.split(" @ ")
		p = tuple([int(n) for n in p.split(", ")[:2]])
		v = tuple([int(n) for n in v.split(", ")[:2]])
		m = v[1] / v[0]
		b = p[1] - m * p[0]
		lines.append((m, b))
		approach_closures.append(generate_is_approaching_closure(p[0], p[1], v))

	# Iterate over all of the intersections between the lines. Count += 1 if the
	# intersection is further along the line from both line's origins. 
	intersections = 0
	for ind_1, line_1 in enumerate(lines):
		for ind_2, line_2 in enumerate(lines[ind_1 + 1:], ind_1 + 1):
			
			# m_ is the slope of line_, b_ is the y-intercept of line_
			m1, b1 = line_1
			m2, b2 = line_2

			# Parallel lines don't cross
			if m1 == m2:
				continue

			# Did some algebra outside of the code and determined this is how
			# the intersection relates. 
			dm = (-m1) - (-m2)
			i = (((-b2) - (-b1)) / dm, (b1 * m2 - b2 * m1) / dm)

			line_1_approaching = approach_closures[ind_1](i) 
			line_2_approaching = approach_closures[ind_2](i)
			converging =  line_1_approaching and line_2_approaching
			
			intersections += 1 if in_bounds(i) and converging else 0

	return intersections

def do_part_two_for(lines):
	pass

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"This is the prompt for Part One of the problem.\n")

	results = do_part_one_for(example_lines, True)
	print(f"When we do part one for the example input:")
	print(f"\tThe number of intersections in the specified region is {results}")
	print(f"\tWe expected: 2\n")

	results = do_part_one_for(input_lines, False)
	print(f"When we do part one for the actual input:")
	print(f"\tThe number of intersections in the specified region is {results}"
	   	  f"\n")

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
	print("--- DAY 24: Never Tell Me The Odds ---\n")
