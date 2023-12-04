# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque
import heapq
import math

_solved_primes_max = 3
_solved_primes = [2, 3]

def is_prime(n:int):
	"""Checks if the number n is a prime number or not."""
	global _solved_primes_max
	global _solved_primes

	# If we are checking if a number is prime, we find if all numbers up to it 
	# are prime. So whenever we call this and we haven't found out if n is prime
	# we will expand our knowledge base of known primes to make find primes less
	# than n a constant lookup for the rest of this session. 
	if n <= _solved_primes_max:
		return n in _solved_primes
	
	# Prime number generation using a sieve of Eratosthenes. 
	sieve = {i:True for i in range(_solved_primes_max, n+1)}

	# Since we're only checking from the last maximum prime we found we need to 
	# pre-filter multiples of all of our known primes. 
	for p in _solved_primes:
		mult = p * p
		while mult <= n:
			sieve[mult] = False
			mult += p

	# Now we do the same thing, but we are checking each number in the sieve 
	# along the way from our previous max prime to the end.
	for p in range(_solved_primes_max + 1, int(math.sqrt(n))+1):
		if sieve[p]:					# If tentatively prime still, is prime
			# All multiples of p: p * x, where x is less than or equal to p have
			# already been filtered in earlier passes. EX: if p is 3, 6 was 
			# filtered out when we filtered all the multiples of 2.
			mult = p * p
			while mult <= n:
				sieve[mult] = False
				mult += p

	# We've filtered out all of the non-primes between _solved_primes_max + 1 to
	# n, because any numbers after sqrt(n) were either filtered out as multiples
	# of numbers smaller than sqrt(n), or were left in because they were prime.
	for p in range(_solved_primes_max + 1, n + 1):
		if sieve[p]:
			_solved_primes.append(p)

	# Update our state tracking and return the answer. 
	_solved_primes_max = n
	return n in _solved_primes


def dijkstra_paths(graph, orig, dests, all_reachable_dests=True):
	"""Uses Dijkstra's algorithm to find paths from the origin in the graph.

	One or more destinations must be specified. Default behaviour for multiple 
	destinations is to return the shortest paths from the origin to each 
	reachable destination. To find a single path, provide a single destination 
	in the dests list, or provide the all_reachable_dests parameter with a False
	value. 

	Nodes in the graph are assumed to have an iterable property called 
	neighbours that stores the keys for the nodes adjacent to them in the 
	graph.

	If there were no reachable destinations, this function raises a LookupError.

	Args:
		graph: A dict mapping identifying node names as keys to node objects. It
			is assumed that the node object has a property called 'neighbours':
			an iterable containing the keys of other nodes that the node object
			can reach in one movement. 
		orig: The key for the node that acts as the starting point for our 
			pathfinding.
		dests: The keys for any points of interest we're trying to find paths 
			for. Must be one or more keys in an iterable.
		all_reachable_dests: Whether or not to find the paths to every reachable
			destination, defaulting to "True". If false, the function will 
			return the shortest path to any destination (the first it finds).
	
	Returns:
		One or more shortest paths through the graph from the origin to a 
		destination. Paths are stored in a list, and each path is a list of the 
		keys for every node along the path, endpoints included.
	
	Raises:
		LookupError: If the function fails to find any paths.
	"""
	# Boiler-plate state tracking. 
	ENTRIES = 0
	unvisited = set(graph.keys())
	search_queue = []
	def extend_search_queue(new_nodes, path):
		nonlocal ENTRIES, unvisited, search_queue
		
		# Assumes we're extending by a list, but can handle extending by a node.
		if not isinstance(new_nodes, list):
			new_nodes = [new_nodes]

		# Including ENTRIES as a tiebreaking value maintains the heap invariant
		for node in new_nodes:
			if node in unvisited:
				new_path = path.copy()
				new_path.append(node)
				search_queue_node = (len(new_path), ENTRIES, node, new_path)
				heapq.heappush(search_queue, search_queue_node)
				ENTRIES += 1

	# Initializing values
	extend_search_queue(orig, [])
	dest_names = set(dests)
	paths = []
	paths_remaining = len(dests) if all_reachable_dests else 1

	# Search the entire space!
	while len(search_queue):
		# dist and tiebreaker are needed by the heap for sorting, but not by us
		dist, tiebreaker, node_name, path = heapq.heappop(search_queue)

		# Skip visited nodes. 
		if node_name not in unvisited:
			continue

		# Count this as a visit and update our records if we need to. 
		unvisited.remove(node_name)
		if node_name in dest_names:
			paths.append(path)
			paths_remaining -= 1
			if not paths_remaining:
				return paths
		
		# If we get here, we need to continue pathfinding.
		extend_search_queue(graph[node_name].neighbours, path)

	# If we get here, we've found all of the paths we could, but at least one of
	# the destinations couldn't be reached. As long as we found at least one 
	# path, return all of the paths we found, otherwise raise a LookupError.
	if len(paths):
		return paths
	else:
		raise LookupError(f"Could not find a path from node {orig} to any of th"
		    			  f"e {len(dests)} destinations in the specified graph")
	

def vector_map_from_string_list(string_list, default_fn=lambda: ".",
								interpreter_fn=lambda x: x) -> defaultdict:
	"""Converts a list of strings into a vector map of objects.

	The map is implemented as an instance of collections.defaultdict so that you
	can refer to points within the map that are not yet defined. The keys for 
	the defaultdict are instances of the utilities.vector class, so that you can
	perform basic arithmetic on them and find neighbouring points easily. Values
	are stored as characters by default, but you can provide a function to 
	interpret the character into some other object if need be. 

	The co-ordinate map is given with the origin as the left-most character of 
	the first string, with x increasing to the left and y increasing downwards

	Args:
		string_list: A list of strings; typically the problem input. 
		default_fn: The default factory function for the defaultdict. This 
			defaults to the character '.', as AoC problems tend to provide that
			as a 'blank space' value in their inputs. 
		interpreter_fn: A function to convert the character into some object you
			wish to use for the problem. The default implementation just spits
			the character back out.
	"""
	vector_map = defaultdict(default_fn)
	for y, string in enumerate(string_list):
		for x, char in enumerate(string):
			vector_map[vector(x, y)] = interpreter_fn(char)
	return vector_map


def prime_factorize(n):
	"""Returns a number as its unique list of prime factors.

	Prime factors are returned as two-tuples of the form (b, e) such that b is 
	the prime factor in question, and e is the power to which it is raised. 
	"""
	# The prime factorization of a prime number is just itself to the power of 1
	# (Sneaky side effect, making this check first guarantees that 
	# _solved_primes is generated up to n)
	if is_prime(n):
		return [(n, 1)]
	
	factors = []
	n_copy = n
	for p in _solved_primes:
		if n_copy == 1:
			break

		p_power = 0
		while not n_copy % p:
			n_copy //= p
			p_power += 1
		
		if p_power > 0:
			factors.append((p, p_power))

	return factors


def print_map(map, translation=lambda x: x, prefix="\t", bounds=40):
	"""Prints a dictionary to a screen for debugging/display purposes.

	Assumes that the keys for each value in the dictionary are of the 
	utilities.vector class, and that those values will be displayed as a 
	single character. The default assumption is that each value will be a
	single character already, and that if it isn't a translation function 
	will be provided that interprets the value as a single character. 

	The printing of the map will start in the top left corner by dynamically 
	determining what the minimum x and y values are and iterating from there. It
	will exhaustively reference every point from the top-left corner to the 
	bottom-right corner, so ensure that it can handle calling any of those keys
	(for instance, make sure it's a default_dict or that it's not sparsely 
	populated).

	Unless otherwise specified, the map should fit into a 40x40 grid of 
	characters, you can specify a different bounding number, but it always 
	interprets the bounds as a square. When provided a map that is larger than 
	the bounding square in one of it's length or width dimensions, this function
	will gracefully exit after printing that the map is too big (this is helpful
	when you want to print the map for the example problem, but not the actual 
	input, for instance)

	Args:
		map: The dictionary to display. 
		translation: A function that is expected to convert the values in map to
			a single character string. Defaults to an identity function.
		prefix: String printed before every row begins. Intended as a way to set
			indentation levels for the map, defaults to a tab character
		bounds: The maximum side length for a map. Setting this to a value less
			than the map size causes the function to gracefully exit. 
	"""
	all_coords = [v for v in map.keys()]
	MINX = all_coords[0].x
	MAXX = all_coords[0].x
	MINY = all_coords[0].y
	MAXY = all_coords[0].y
	for xy in all_coords:
		MINX = min(MINX, xy.x)
		MAXX = max(MAXX, xy.x)
		MINY = min(MINY, xy.y)
		MAXY = max(MAXY, xy.y)

	if MAXX - MINX > bounds or MAXY - MINY > bounds:
		print(f"[Couldn't render map in a {bounds}x{bounds} square or less]\n")
		return

	for y in range(MINY, MAXY+1):
		print(prefix, end="")
		for x in range(MINX, MAXX+1):
			print(f"{translation(map[vector(x,y)])}", end="")
		print()
	print()
	return


