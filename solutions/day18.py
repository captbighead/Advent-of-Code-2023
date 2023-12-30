# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

try:
	input_lines = io.read_input_as_lines(18)
	example_lines = io.read_example_as_lines(18)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]

def do_part_one_for_slow(lines, ex=False):
	position = vector()
	udlr = vector.LOOKUP_UDLR()

	# Grid of cubes and whether or not they have been dug out. 
	grid = defaultdict(lambda: False)
	grid[position] = True

	# Dig out the trench:
	for line in lines:
		dir_c, dist, discard = line.split()
		dist = int(dist)
		dir = udlr[dir_c]
		for i in range(dist):
			position += dir
			grid[position] = True

	# After visual inspection, I've determined that the point (1, 1) is in the 
	# polygon for both test cases. 
	visited = set()
	flood_fill_queue = deque([vector(1, 1)])
	while len(flood_fill_queue):
		next = flood_fill_queue.popleft()
		if next in visited:
			continue
		visited.add(next)
		
		grid[next] = True
		for n in next.adjacents:
			if not grid[n] and n not in visited:
				flood_fill_queue.append(n)
	
	return len([v for v in grid.keys() if grid[v]])

def do_part_one_for(lines):
	dirs = vector.LOOKUP_UDLR()
	posn = vector()
	area = 0

	perim_dist = 0
	for ln in lines:
		dir_c, dist, discard = ln.split()
		
		dist = int(dist)
		dir = dirs[dir_c]

		next = posn + (dir * dist)
		area += next.x * posn.y - posn.x * next.y
		perim_dist += dist
		posn = next

	next = vector()
	area += next.x * posn.y - posn.x * next.y
	perim_dist += next.distance(posn)

	return abs(area // 2) + perim_dist // 2 + 1

def do_part_two_for(lines):
	dirs = vector.UNIT_VECTORS()
	posn = vector()
	area = 0

	perim_dist = 0
	for ln in lines:
		discard_1, discard_2, hex_encoded = ln.split()
		hex_encoded = algos.erase(hex_encoded, ["(", ")", "#"])
		
		dir = dirs[(int(hex_encoded[-1]) + 1) % 4]
		dist = int(hex_encoded[:-1], 16)

		next = posn + (dir * dist)
		area += next.x * posn.y - posn.x * next.y
		perim_dist += dist
		posn = next

	next = vector()
	area += next.x * posn.y - posn.x * next.y
	perim_dist += next.distance(posn)

	return abs(area // 2) + perim_dist // 2 + 1

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"This is the prompt for Part One of the problem.\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe total cubes of lava that fit in the trench is {results}")
	print(f"\tWe expected: 62\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe total cubes of lava that fit in the trench is {results}")
	print(f"\tWe expected: 52055 (because we've solved it before)\n")


def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"This is the prompt for Part Two of the problem.\n")

	results = do_part_two_for(example_lines)
	print(f"When we do part two for the example input:")
	print(f"\tThe number of cubes of lava that can fit in the trench is "
		  f"{results}")
	print(f"\tWe expected: 952408144115\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe number of cubes of lava that can fit in the trench is "
		  f"{results}\n")

def print_header():
	print("--- DAY 18: Lavaduct Lagoon ---\n")
