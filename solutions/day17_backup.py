# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

import heapq

try:
	input_lines = io.read_input_as_lines(17)
	example_lines = io.read_example_as_lines(17)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]

class SNode:

	best_visits = defaultdict(lambda: 999999999)

	def __init__(self, posn: vector, running_heat, path, grid) -> None:
		self.posn = posn
		self.running_heat = running_heat
		self.path = path
		self.grid = grid
		SNode.best_visits[posn] = min(SNode.best_visits[posn], running_heat)

	def neighbours(self):
		can_go_straight = True
		if len(self.path) >= 3:
			last_3_moves = set(self.path[-3:])
			can_go_straight = len(last_3_moves) > 1
		
		last_dir = self.path[-1] if len(self.path) else vector.RIGHT()
		options = [last_dir.rotate_ccw(1), last_dir.rotate_cw(1)]
		if can_go_straight:
			options.insert(0, last_dir)

		neighbours = []
		for opt in options:
			spec = opt + self.posn
			if SNode.best_visits[spec] < self.running_heat + self.grid[spec]:
				continue
			spec_heat = self.running_heat + self.grid[spec]
			spec_path = self.path.copy()
			spec_path.append(opt)
			neighbours.append(SNode(spec, spec_heat, spec_path, self.grid))
		return neighbours
		



def do_part_one_for(lines):
	df = lambda: 999999999
	gridmap = algos.vector_map_from_string_list(lines, default_fn=df, 
											 	interpreter_fn=int)
	
	orig = vector()
	dest = vector(len(lines[0]) - 1, len(lines) - 1)

	# Boiler-plate state tracking. 
	ENTRIES = 0
	unvisited = set(gridmap.keys())
	search_queue = []
	def extend_search_queue(new_nodes):
		nonlocal ENTRIES, unvisited, search_queue
		
		# Assumes we're extending by a list, but can handle extending by a node.
		if not isinstance(new_nodes, list):
			new_nodes = [new_nodes]

		# Including ENTRIES as a tiebreaking value maintains the heap invariant
		for node in new_nodes:
			node: SNode
			search_queue_node = (node.running_heat, ENTRIES, node)
			heapq.heappush(search_queue, search_queue_node)
			ENTRIES += 1

	# Initializing values
	extend_search_queue(SNode(orig, 0, [], gridmap))

	# Search the entire space!
	while len(search_queue):
		# dist and tiebreaker are needed by the heap for sorting, but not by us
		dist, tiebreaker, node = heapq.heappop(search_queue)
		node:SNode

		# Count this as a visit and update our records if we need to. 
		if node.posn == dest:
			continue
		
		# If we get here, we need to continue pathfinding.
		extend_search_queue(node.neighbours())
	
	return SNode.best_visits[dest]
			


def do_part_two_for(lines):
	pass

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"Shortest path through grid where you can't go backwards, only left,"
	   	  f" right or forwards, and you can only go 3 steps forward before a tu"
		  f"rn.\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe least possible heat loss is {results}")
	print(f"\tWe expected: 102\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe least possible heat loss is {results}\n")

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
	print("--- DAY 17: <TITLE GOES HERE> ---\n")
