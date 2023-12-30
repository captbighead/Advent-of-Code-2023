# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

import itertools
import random
import time

try:
	input_lines = io.read_input_as_lines(25)
	example_lines = io.read_example_as_lines(25)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]


class Graph_Rewrite:

	EDGE_ID = 0

	def __init__(self) -> None:
		self.vertices = set()
		
		# Edges stored as tuple of (v, w, ID) (to allow duplicate edges)
		# v, w are in ascending order
		self.edges = set()

		# Lookup stores all the edge IDs for duplicates of a given edge
		self.edge_lookup = defaultdict(list)

		# And of course we'll need a way to look up edges by vertices. We won't
		# need the inverse because we have both of the vertices needed *in* the
		# edge.
		self.edges_by_vertices = defaultdict(set)

	def add_vertex(self, name):
		self.vertices.add(name)
	
	def add_edge(self, v, w):
		# All edges *must* be stored in ascending order of vertices to ensure 
		# undirected-ness
		mn = min(v, w)
		mx = max(v, w)

		if self.edge_lookup[(mn, mx)]:
			return	# Edge already exists.  

		self.edges.add((mn, mx, Graph_Rewrite.EDGE_ID))
		self.edge_lookup[(mn, mx)].append(Graph_Rewrite.EDGE_ID)
		self.edges_by_vertices[v].add((mn, mx, Graph_Rewrite.EDGE_ID))
		self.edges_by_vertices[w].add((mn, mx, Graph_Rewrite.EDGE_ID))
		Graph_Rewrite.EDGE_ID += 1

	def random_contraction(self):
		random.seed(69420)
		v, w, *selected_id = self.edges.pop()
		#v, w, *selected_id = random.sample(self.edges, k=1).pop()
		
		# Create the super-node
		vw = f"{v}|{w}"
		self.vertices.add(vw)

		# Remove the newly self-referential edges
		for eid in self.edge_lookup[(v, w)]:
			self.edges.discard((v, w, eid))
			self.edges_by_vertices[v].remove((v, w, eid))
			self.edges_by_vertices[w].remove((v, w, eid))
		self.edge_lookup.pop((v, w))

		# Replace every edge to v with an edge to vw:
		to_replace = self.edges_by_vertices[v].union(self.edges_by_vertices[w])
		for old_v, old_w, old_id in to_replace:
			# We're keeping one of these, but ditching another.
			old_kept = old_w if old_v in (v, w) else old_v
			mn = min(old_kept, vw)
			mx = max(old_kept, vw)

			# Remove the old version (including the lookup): 
			self.edges_by_vertices[old_kept].remove((old_v, old_w, old_id))
			self.edges.remove((old_v, old_w, old_id))
			self.edge_lookup[(old_v, old_w)].append("Don't matter")
			self.edge_lookup.pop((old_v, old_w))

			# Add the new version: 
			self.edges_by_vertices[old_kept].add((mn, mx, old_id))
			self.edges_by_vertices[vw].add((mn, mx, old_id))
			self.edges.add((mn, mx, old_id))
			self.edge_lookup[(mn, mx)].append(old_id)
		
		# Finally, remove the old edged that used to exist for v and w, and then
		# remove v and w.
		self.edges_by_vertices.pop(v)
		self.edges_by_vertices.pop(w)
		self.vertices.remove(v)
		self.vertices.remove(w)

def rebuild_graph(graph_defs):
	graph = Graph_Rewrite()
	for ln in graph_defs:
		tokens = algos.erase(ln, ":").split()
		primary = tokens[0]
		graph.add_vertex(primary)
		for secondary in tokens[1:]:
			graph.add_vertex(secondary)
			graph.add_edge(primary, secondary)
	return graph

def do_part_one_for(lines):
	iterations = 0
	while True:
		iterations += 1

		graph = rebuild_graph(lines)
		while len(graph.vertices) > 2:
			graph.random_contraction()
		
		a, b = list(graph.vertices)
		if len(graph.edges_by_vertices[a]) == 3:
			print(f"\tSolution found after {iterations} iterations!")
			return (a.count("|") + 1) * (b.count("|") + 1)

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"Find the set of three wires that bisects the connected widgets and "
	   	  f"doodads.\n")
	
	print(f"NOTE: This is a randomized algorithm. You could be sitting here for"
	   	  f" 10 minutes, or 10 seconds. :/\n")

	print(f"When we do part one for the example input:")
	results = do_part_one_for(example_lines)
	print(f"\tThe product of the sizes of the new subsystems is {results}")
	print(f"\tWe expected: 54\n")

	print(f"When we do part one for the actual input:")
	results = do_part_one_for(input_lines)
	print(f"\tThe product of the sizes of the new subsystems is {results}\n")

def solve_p2():
	print("Day 25 has no part two! :)\n\nMerry Christmas!\n")
	
def print_header():
	print("--- DAY 25: Snowverload ---\n")
