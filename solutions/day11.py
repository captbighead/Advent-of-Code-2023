# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

try:
	input_lines = io.read_input_as_lines(11)
	example_lines = io.read_example_as_lines(11)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]

def expand_space(space_defs):
	y_expansions = []
	x_expansions = []
	# Find expansion points
	for y in range(len(space_defs)):
		if space_defs[y].count(".") == len(space_defs):
			y_expansions.append(y)
	for x in range(len(space_defs[0])):
		empty = True
		for y in range(len(space_defs)):
			empty = empty and space_defs[y][x] == "."
		if empty:
			x_expansions.append(x)

	# Apply expansions. 
	new_lines = []
	for y in range(len(space_defs)):
		line_str = ""
		for x in range(len(space_defs[y])):
			line_str += space_defs[y][x]
			if x in x_expansions:
				line_str += "."
		new_lines.append(line_str)
		if y in y_expansions:
			new_lines.append(line_str) 
	return new_lines


def do_part_one_for(lines):
	space = expand_space(lines)
	space = algos.vector_map_from_string_list(space)
	planets = [v for v in space.keys() if space[v] != "."]
	
	summation = 0
	for i, pi in enumerate(planets):
		for pj in planets[i+1:]:
			summation += pi.distance(pj)
	return summation


def do_part_two_for(lines, expansion_factor=999999):
	y_expansions = []
	x_expansions = []
	# Find expansion points
	for y in range(len(lines)):
		if lines[y].count(".") == len(lines):
			y_expansions.append(y)
	for x in range(len(lines[0])):
		empty = True
		for y in range(len(lines)):
			empty = empty and lines[y][x] == "."
		if empty:
			x_expansions.append(x)
	
	space = algos.vector_map_from_string_list(lines)
	planets_pre_expansion = [v for v in space.keys() if space[v] != "."]
	planets = []
	for planet in planets_pre_expansion:
		planet: vector
		x_modifier = 0
		y_modifier = 0
		for x_exp in x_expansions:
			if x_exp < planet.x:
				x_modifier += expansion_factor
		for y_exp in y_expansions:
			if y_exp < planet.y:
				y_modifier += expansion_factor
		planets.append(vector(planet.x + x_modifier, planet.y + y_modifier))

	summation = 0
	for i, pi in enumerate(planets):
		for pj in planets[i+1:]:
			summation += pi.distance(pj)
	return summation


def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"This is the prompt for Part One of the problem.\n")

	results = do_part_two_for(example_lines, 1)
	print(f"When we do part one for the example input:")
	print(f"\tThe shortest path between every pair of galaxies is {results}")
	print(f"\tWe expected: 374\n")

	results = do_part_two_for(input_lines, 1)
	print(f"When we do part one for the actual input:")
	print(f"\tThe shortest path between every pair of galaxies is {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"This is the prompt for Part Two of the problem.\n")

	results = do_part_two_for(example_lines, 99)
	print(f"When we do part two for the example input:")
	print(f"\tThe sum of the shortest paths between all galaxies is {results}")
	print(f"\tWe expected: 8410\n")

	results = do_part_two_for(input_lines, 999999)
	print(f"When we do part two for the actual input:")
	print(f"\tThe sum of the shortest paths between all galaxies is {results}"
	   	  f"\n")

def print_header():
	print("--- DAY 11: Cosmic Expansion ---\n")
