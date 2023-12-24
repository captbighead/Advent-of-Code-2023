# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

import time

try:
	input_lines = io.read_input_as_lines(23)
	example_lines = io.read_example_as_lines(23)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]

class Graph:

	NEXT_VERTEX = 1

	class Vertex:

		def __init__(self, position: vector) -> None:
			self.position = position
			self.id = Graph.NEXT_VERTEX
			Graph.NEXT_VERTEX += 1
			
			self.name = ""
			id_for_name_gen = self.id
			while id_for_name_gen > 0:
				self.name = chr((id_for_name_gen - 1) % 26 + 65) + self.name
				id_for_name_gen -= (id_for_name_gen - 1) % 26
				id_for_name_gen //= 26
		
		def __eq__(self, __value: object) -> bool:
			return isinstance(__value, Graph.Vertex) and self.id == __value.id
		
		def __hash__(self) -> int:
			return hash(self.id)

		def __repr__(self) -> str:
			return self.name + str(self.position)
			

	def __init__(self) -> None:
		self.vertices = set()
		self.vertices_by_position = {}
		self.edge_matrix = {}
		self.edges_by_vertex = defaultdict(list)

	def add_vertex(self, position: vector) -> 'Graph.Vertex':
		if self.vertices_by_position.get(position, False):
			raise KeyError(f"Vertex already exists for {position}")
		new = Graph.Vertex(position)
		self.vertices.add(new)
		self.vertices_by_position[position] = new
		return new
	
	def get_vertex(self, position: vector):
		if not self.vertices_by_position.get(position, False):
			self.add_vertex(position)
		return self.vertices_by_position[position]
	
	def is_vertex(self, position: vector):
		return position in self.vertices_by_position.keys()

	def add_edge(self, vertex_a: 'Graph.Vertex', vertex_b: 'Graph.Vertex', 
			  	 cost: int) -> None:
		self.edge_matrix[vertex_a, vertex_b] = cost
		self.edges_by_vertex[vertex_a].append((vertex_b, cost))
		self.edges_by_vertex[vertex_a].sort(key=lambda t: t[1], reverse=True)

	def get_edges(self, vertex: 'Graph.Vertex') -> 'list':
		return self.edges_by_vertex[vertex]

def do_part_one_for(lines):
	Graph.NEXT_VERTEX = 1
	graph = Graph()
	grid = algos.vector_map_from_string_list(lines, default_fn=lambda: "#")
	orig = vector(1, 0)
	dest = vector(len(lines[0]) - 2, len(lines) - 1)
	graph.add_vertex(orig)
	traversal_queue = deque()
	traversal_queue.append(([orig, orig+vector.DOWN()], graph.get_vertex(orig)))

	passibility = {
		">": lambda v: v == vector.RIGHT(), 
		"<": lambda v: v == vector.LEFT(),
		"^": lambda v: v == vector.UP(), 
		"v": lambda v: v == vector.DOWN(),
		".": lambda v: True,
		"#": lambda v: False
	}

	visited = set()
	while traversal_queue:
		path, last_vertex = traversal_queue.pop()
		this_tile = path[-1]

		if last_vertex.position == vector(13, 19) and this_tile.x < 13:
			this_tile = this_tile

		# Check if we've been here before or not. 
		if this_tile in visited and not graph.is_vertex(this_tile):
			continue
		visited.add(this_tile)

		# This is a vertex if there's more than one way in/out of it
		paths_out = sum(1 for adj in this_tile.adjacents if grid[adj] != "#")

		# Process it differently if it's a vertex or not. Vertices indicate the 
		# end of an edge, and we need to define it in the graph. 
		if paths_out > 2 or this_tile == dest:
			this_vertex = graph.get_vertex(this_tile) 

			if last_vertex.position == vector(13, 19):
				this_tile = this_tile

			# Follow the path from the beginning to this. If a tile is a 
			# directed tile, then this is a directed edge. Mark it as such. Then
			# we can record if it's directed from Last to This or vice-versa. 
			directed = False
			directed_in_reverse = False
			for i, v in enumerate(path[1:]):
				dir = v - path[i]
				directed = directed or grid[v] in "<>v^"
				directed_in_reverse = directed and not passibility[grid[v]](dir)
				if directed:
					break
			
			# Now add the edges to our graph: 
			path_len = len(path) - 1
			if directed and directed_in_reverse:
				graph.add_edge(this_vertex, last_vertex, path_len)
			elif directed and not directed_in_reverse:
				graph.add_edge(last_vertex, this_vertex, path_len)
			else:
				graph.add_edge(this_vertex, last_vertex, path_len)
				graph.add_edge(last_vertex, this_vertex, path_len)

			last_vertex = this_vertex
			path = [this_tile]

		# Then, regardless of if we're a vertex, the next step is the same. 
		for adj in this_tile.adjacents:
			if grid[adj] != "#" and adj not in path:
				adj_path = path.copy()
				adj_path.append(adj)
				traversal_queue.append((adj_path, last_vertex))

	best = 0
	visited = set()
	search_stack = [(graph.get_vertex(orig), [graph.get_vertex(orig)], 0)]
	while search_stack:
		this_vertex, this_path, this_cost = search_stack.pop()
		if this_vertex.position == dest:
			best = max(best, this_cost)
			continue

		if (this_vertex, this_cost) not in visited:
			visited.add((this_vertex, this_cost))
			edges = graph.edge_matrix
			nexts = [(w, c) for (v, w), c in edges.items() if v == this_vertex]
			nexts = sorted(nexts, key=lambda wc: wc[1], reverse=True)
			for next_vertex, next_cost in nexts:
				if next_vertex not in this_path:
					next_cost += this_cost
					next_path = this_path.copy()
					next_path.append(next_vertex)
					search_stack.append((next_vertex, next_path, next_cost))

	return best

def do_part_two_for(lines):
	start_time = time.time()
	new_lines = []
	for ln in lines:
		for slope in "><v^":
			ln = ln.replace(slope, ".")
		new_lines.append(ln)
	lines = new_lines

	Graph.NEXT_VERTEX = 1
	graph = Graph()
	grid = algos.vector_map_from_string_list(lines, default_fn=lambda: "#")
	orig = vector(1, 0)
	dest = vector(len(lines[0]) - 2, len(lines) - 1)
	graph.add_vertex(orig)
	traversal_queue = deque()
	traversal_queue.append(([orig, orig+vector.DOWN()], graph.get_vertex(orig)))

	passibility = {
		">": lambda v: v == vector.RIGHT(), 
		"<": lambda v: v == vector.LEFT(),
		"^": lambda v: v == vector.UP(), 
		"v": lambda v: v == vector.DOWN(),
		".": lambda v: True,
		"#": lambda v: False
	}

	visited = set()
	while traversal_queue:

		path, last_vertex = traversal_queue.pop()
		this_tile = path[-1]

		if last_vertex.position == vector(13, 19) and this_tile.x < 13:
			this_tile = this_tile

		# Check if we've been here before or not. 
		if this_tile in visited and not graph.is_vertex(this_tile):
			continue
		visited.add(this_tile)

		# This is a vertex if there's more than one way in/out of it
		paths_out = sum(1 for adj in this_tile.adjacents if grid[adj] != "#")

		# Process it differently if it's a vertex or not. Vertices indicate the 
		# end of an edge, and we need to define it in the graph. 
		if paths_out > 2 or this_tile == dest:
			this_vertex = graph.get_vertex(this_tile) 

			if last_vertex.position == vector(13, 19):
				this_tile = this_tile

			# Follow the path from the beginning to this. If a tile is a 
			# directed tile, then this is a directed edge. Mark it as such. Then
			# we can record if it's directed from Last to This or vice-versa. 
			directed = False
			directed_in_reverse = False
			for i, v in enumerate(path[1:]):
				dir = v - path[i]
				directed = directed or grid[v] in "<>v^"
				directed_in_reverse = directed and not passibility[grid[v]](dir)
				if directed:
					break
			
			# Now add the edges to our graph: 
			path_len = len(path) - 1
			if directed and directed_in_reverse:
				graph.add_edge(this_vertex, last_vertex, path_len)
			elif directed and not directed_in_reverse:
				graph.add_edge(last_vertex, this_vertex, path_len)
			else:
				graph.add_edge(this_vertex, last_vertex, path_len)
				graph.add_edge(last_vertex, this_vertex, path_len)

			last_vertex = this_vertex
			path = [this_tile]

		# Then, regardless of if we're a vertex, the next step is the same. 
		for adj in this_tile.adjacents:
			if grid[adj] != "#" and adj not in path:
				adj_path = path.copy()
				adj_path.append(adj)
				traversal_queue.append((adj_path, last_vertex))

	best = 0
	visited = set()
	search_stack = [(graph.get_vertex(orig), tuple([graph.get_vertex(orig)]), 0)]
	while search_stack:

		this_vertex, this_path, this_cost = search_stack.pop()
		this_path = list(this_path)
		if this_vertex.position == dest:
			best = max(best, this_cost)
			continue

		if (this_vertex, tuple(this_path), this_cost) not in visited:
			visited.add((this_vertex, tuple(this_path), this_cost))
			#edges = graph.edge_matrix
			#nexts = [(w, c) for (v, w), c in edges.items() if v == this_vertex]
			#nexts = sorted(nexts, key=lambda wc: wc[1], reverse=True)
			nexts = graph.get_edges(this_vertex)
			for next_vertex, next_cost in nexts:
				if next_vertex not in this_path:
					next_cost += this_cost
					next_path = this_path.copy()
					next_path.append(next_vertex)
					search_stack.append((next_vertex, tuple(next_path), next_cost))

	return best

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"This is the prompt for Part One of the problem.\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe longest path possible without repeats is {results}")
	print(f"\tWe expected: 94\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe longest path possible without repeats is is {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"Do it again, but without slopes!\n")

	results = do_part_two_for(example_lines)
	print(f"When we do part two for the example input:")
	print(f"\tThe longest path is {results}")
	print(f"\tWe expected: 154\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe longest path is {results}\n")

def print_header():
	print("--- DAY 23: A Long Walk ---\n")
