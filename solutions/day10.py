# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

try:
	input_lines = io.read_input_as_lines(10)
	example_lines = io.read_example_as_lines(10)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]

example_lines_2 = ["..........", ".S------7.", ".|F----7|.", ".||....||.", 
				   ".||....||.", ".|L-7F-J|.", ".|..||..|.", ".L--JL--J.", 
				   ".........."]

CONNECTIONS_LOOKUP = {
		"F": set([vector.RIGHT(), vector.DOWN()]),
		"J": set([vector.LEFT(), vector.UP()]),
		"L": set([vector.RIGHT(), vector.UP()]),
		"7": set([vector.LEFT(), vector.DOWN()]),
		"-": set([vector.RIGHT(), vector.LEFT()]),
		"|": set([vector.UP(), vector.DOWN()]),
		".": set()
	}

ENHANCE_LOOKUP = {
		"F": [vector(1, 1), vector(2, 1), vector(1, 2)],
		"J": [vector(1, 1), vector(0, 1), vector(1, 0)],
		"L": [vector(1, 1), vector(2, 1), vector(1, 0)],
		"7": [vector(1, 1), vector(0, 1), vector(1, 2)],
		"-": [vector(1, 1), vector(0, 1), vector(2, 1)],
		"|": [vector(1, 1), vector(1, 0), vector(1, 2)],
		".": set()
	}

def extract_loop(noisy_map):
	start = [v for v in noisy_map.keys() if noisy_map[v] == 'S'][0]

	# Find out what kind of tile the start position is. (Visual inspection 
	# of the inputs tells me that the noisy tiles beside the start don't connect
	# to it)
	start_conns = set()
	for u in vector.UNIT_VECTORS():	# Which unit vectors connect to start?
		v = start + u
		if u * -1 in CONNECTIONS_LOOKUP[noisy_map[v]]:
			start_conns.add(u)

	# What's the tile type with those connections? 
	for tile_type in CONNECTIONS_LOOKUP.keys():
		if CONNECTIONS_LOOKUP[tile_type] == start_conns:
			noisy_map[start] = tile_type
			break

	# Pick a direction from the start and iterate around the loop. 
	loop = [start, start_conns.pop() + start]
	while loop[-1] != loop[0]:
		next_tile = noisy_map[loop[-1]]
		for conn in CONNECTIONS_LOOKUP[next_tile]:
			if conn + loop[-1] != loop[-2]:
				loop.append(conn + loop[-1])
				break
	
	return loop


def do_part_one_for(lns):
	noisy = algos.vector_map_from_string_list(lns)
	loop = extract_loop(noisy)
	return len(loop) // 2


def do_part_two_for(lns, ex=True):
	noisy = algos.vector_map_from_string_list(lns)
	loop = extract_loop(noisy)

	# Translate the noisy map into a clean version at the proper resolution. 
	regular_map = defaultdict(lambda: ".")
	for v in loop:
		regular_map[v] = noisy[v]
	
	# The trick to the identification of the interior cells is that we can 
	# 'squeeze' through adjacent pipes, which I can't think of how to code 
	# cleanly. But if we 'zoom and enhance' the image so that each tile becomes 
	# a set of 3x3 tiles, suddenly there are gaps between the pipes. 
	x_rng = (min(v.x for v in loop), max(v.x for v in loop))
	y_rng = (min(v.y for v in loop), max(v.y for v in loop))
	big_map = defaultdict(lambda: "#")
	for Y in range(y_rng[0], y_rng[1] + 1):
		for X in range(x_rng[0], x_rng[1] + 1):
			symbol = regular_map[vector(X, Y)]
			for y in range(3):
				for x in range(3):
					abs = vector(x + X*3, y + Y*3)
					rel = vector(x, y)
					big_map[abs] = "#" if rel in ENHANCE_LOOKUP[symbol] else "I"

	# Seed the search_queue with the top left corner of bigmap. Pull everything
	# from the queue, flagging it as exterior and adding its non-wall neighbours
	# that haven't been seen as exterior as well. 
	visited = set()
	search_queue = deque([vector(x_rng[0]*3, y_rng[0]*3)])
	while len(search_queue):
		v = search_queue.popleft()
		if v in visited:
			continue
		big_map[v] = "E"
		visited.add(v)
		for u in vector.UNIT_VECTORS():
			if u + v not in visited and big_map[u + v] != "#":
				search_queue.append(u + v)

	# Now, all that couldn't be reached from an exterior node is an interior 
	# node. Looping over the coordinates of the regular map, check if the 
	# corresponding subregion in the big map is interior. To speed things up, 
	# you only need to check the middle square
	for V in regular_map.keys():
		if regular_map[V] != ".":
			continue
		v = V * 3 + vector.DOWN() + vector.RIGHT()
		regular_map[V] = big_map[v]
	
	return len([v for v in regular_map.values() if v == "I"])



def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"This is the prompt for Part One of the problem.\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe distance (moving through the pipe loop) to the furthest point"
	   	  f" in the loop from the start is {results} steps.")
	print(f"\tWe expected: 8\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe distance (moving through the pipe loop) to the furthest point"
	   	  f" in the loop from the start is {results} steps.\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"How many tiles are completely enclosed in the interior of the loop"
	   	  f"?\n")

	results = do_part_two_for(example_lines_2)
	print(f"When we do part two for the example input:")
	print(f"\tThe number of enclosed tiles is {results}")
	print(f"\tWe expected: 4\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe number of enclosed tiles is {results}\n")

def print_header():
	print("--- DAY 10: Pipe Maze ---\n")
