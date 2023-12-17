# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

try:
	input_lines = io.read_input_as_lines(16)
	example_lines = io.read_example_as_lines(16)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]

DEBUG_MODE = False

def do_part_one_for(lines, start_pos=vector(), start_dir=vector.RIGHT()):
	VR, VD, VL, VU = vector.RIGHT(), vector.DOWN(), vector.LEFT(), vector.UP()
	
	gridmap = algos.vector_map_from_string_list(lines, default_fn=lambda: "#")
	energized = {v: False for v in gridmap.keys()}

	visited = set()
	search_space = deque([(start_pos, start_dir)])

	def enqueue_if_legal(position, direction):
		# Helper function handles pruning branches if visited or dead end walls
		next = position + direction
		if gridmap[next] == "#" or (next, direction) in visited:
			return
		search_space.append((next, direction))

	while len(search_space):
		position, direction = search_space.popleft()
		visited.add((position, direction))

		# Energize the new cell. 
		energized[position] = True

		# Decide on movement to next cell based on the structure in this cell
		current_tile_type = gridmap[position]

		# No structure
		if current_tile_type == ".":
			enqueue_if_legal(position, direction)
		
		# L/R Splitter
		elif current_tile_type == "-":
			# Moving parallel to the splitter's type is just normal movement
			if direction in (VR, VL):
				enqueue_if_legal(position, direction)

			# Whereas orthoganl movement becomes two moves: left, right
			else:
				enqueue_if_legal(position, VL)
				enqueue_if_legal(position, VR)
		
		# U/D Splitter
		elif current_tile_type == "|":
			# Moving parallel to the splitter's type is just normal movement
			if direction in (VU, VD):
				enqueue_if_legal(position, direction)

			# Whereas orthoganl movement becomes two moves: up, down
			else:
				enqueue_if_legal(position, VU)
				enqueue_if_legal(position, VD)
		
	
		# Left-hand-tilted mirror
		elif current_tile_type == "\\":
			if direction == VR:
				direction = VD
			elif direction == VU:
				direction = VL
			elif direction == VD:
				direction = VR
			elif direction == VL:
				direction = VU
			enqueue_if_legal(position, direction)
		
		# Right-hand-tilted mirror is the opposite
		elif current_tile_type == "/":
			if direction == VR:
				direction = VU
			elif direction == VU:
				direction = VR
			elif direction == VD:
				direction = VL
			elif direction == VL:
				direction = VD
			enqueue_if_legal(position, direction)

		if DEBUG_MODE:
			printed = gridmap.copy()
			for v in energized.keys():
				if energized[v]:
					printed[v] = "O"
			algos.print_map(printed)
			input()
	
	return len([v for v in energized.keys() if energized[v]])

def do_part_two_for(lines):
	best = 0

	MAX_Y = len(lines)
	MAX_X = len(lines[0])
	for x in range(MAX_X):
		start_pos_top = vector(x, 0)
		start_dir_top = vector.DOWN()
		best = max(best, do_part_one_for(lines, start_pos_top, start_dir_top))

		start_pos_bot = vector(x, MAX_Y)
		start_dir_bot = vector.UP()
		do_part_one_for(lines, start_pos_bot, start_dir_bot)
		best = max(best, do_part_one_for(lines, start_pos_bot, start_dir_bot))

	for y in range(MAX_Y):
		start_pos_lft = vector(0, y)
		start_dir_lft = vector.RIGHT()
		best = max(best, do_part_one_for(lines, start_pos_lft, start_dir_lft))

		start_pos_rgt = vector(MAX_X, y)
		start_dir_rgt = vector.UP()
		do_part_one_for(lines, start_pos_rgt, start_dir_rgt)
		best = max(best, do_part_one_for(lines, start_pos_rgt, start_dir_rgt))

	return best


def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"This is the prompt for Part One of the problem.\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe energized tiles in the grid add to give {results}")
	print(f"\tWe expected: 46\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe energized tiles in the grid add to give {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"This is the prompt for Part Two of the problem.\n")

	results = do_part_two_for(example_lines)
	print(f"When we do part two for the example input:")
	print(f"\tThe best energy results from any starting postion is {results}")
	print(f"\tWe expected: 51\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe best energy results from any starting postion is {results}\n")

def print_header():
	print("--- DAY 16: The Floor Will Be Lava ---\n")
