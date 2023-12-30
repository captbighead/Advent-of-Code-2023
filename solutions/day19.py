# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

try:
	input_lines = io.read_input_as_lines(19)
	example_lines = io.read_example_as_lines(19)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]

def gen_closure(test_def):
	# An test is [x, m, a, s][>, <][<constant literal>]
	test_property = test_def[0]
	test_constant = int(test_def[2:])
	
	if test_def[1] == ">":
		return lambda part_dict: part_dict[test_property] > test_constant
	elif test_def[1] == "<":
		return lambda part_dict: part_dict[test_property] < test_constant
	else:
		raise ValueError(f"Andrew didn't expect this test: {test_def}")

def do_part_one_for(lines):
	processing_workflows = True
	workflows = {}
	part_dicts = []

	for defn in lines:
		if defn == "":
			processing_workflows = False
			continue

		if processing_workflows:
			wf_name, wf_body = defn.split("{")
			wf_rule_defs = wf_body[:-1].split(",")
			wf_rule_checks = []
			for i, rule_def in enumerate(wf_rule_defs):
				# The default destination at the end of the list has no test. 
				if i == len(wf_rule_defs) -1:
					wf_rule_checks.append((lambda obj: True, rule_def))
					break
				test_def, dest = rule_def.split(":")
				wf_rule_checks.append((gen_closure(test_def), dest))
			workflows[wf_name] = wf_rule_checks
			continue

		defn = algos.erase(defn, "{}").replace("=", " ")
		props = defn.split(",")
		part_dict = {}
		for prop_str in props:
			prop, val = prop_str.split()
			part_dict[prop] = int(val)
		part_dicts.append(part_dict)
			
	
	accepted_rejected = {"A": [], "R": []}
	for part in part_dicts:
		current_wf = "in"
		while current_wf not in "AR":
			wf_tests = workflows[current_wf]
			for test, dest in wf_tests:
				if test(part):
					current_wf = dest
					break
		accepted_rejected[current_wf].append(part)
	
	summation = 0
	for part in accepted_rejected["A"]:
		summation += sum(part.values())
	return summation

class graph_node:

	def __init__(self, name, check_num, def_str, registry) -> None:
		self.name = name
		self.check_num = check_num
		self.registry = registry

		if def_str.find(":") != -1:
			self.checked_id = def_str[0]
			def_val, def_dest = def_str[2:].split(":")
			def_val = int(def_val)
			self.upper = 4000 if def_str[1] == ">" else def_val - 1
			self.lower = 1 if def_str[1] == "<" else def_val + 1
			self.dest_true = (def_dest, 0)
			self.dest_false = (name, check_num + 1)
		else:
			# Could check against anything, it all goes to the same place.
			self.checked_id = "x"	
			self.upper = 4000
			self.lower = 1
			self.dest_true = (def_str, 0)
			self.dest_false = (def_str, 0)

		registry[(name, check_num)] = self

def split_ranges(node, xmas):
	comb = tuple(sorted(node + xmas))

	# If the second element is the maximum value of either range, then the two
	# ranges are disjoint. Otherwise, the second element is our lower-bound for
	# the intersection and the third is our upper bound. 
	inner = tuple(comb[1:3]) if comb[1] not in (node[1], xmas[1]) else None

	# The exception to the above rule is if they intersect by exactly one 
	# element, so check for that just in case:
	if inner == None and comb[1] == comb[2]:
		inner = (comb[1], comb[2])
	
	# If it was disjoint, then we return False to indicate the following list of
	# ranges is being handled as a negative, and then we give a list of one: the
	# input range
	if inner == None:
		return (False, [xmas])

	# If we get here, then we know we're returning True, with at least one 
	# range in the list. But there are between 0-2 ranges that *didn't* fit. 
	# We'll append them to the list (if they exist) so that our intersection 
	# range is first, and all applicable outer ranges come after.
	ret_ranges = [inner]

	# If the first of the combined tuple is the first of xmas, then it began on
	# or before the node range.
	if comb[0] == xmas[0]:
		lower = (comb[0], comb[1] - 1)	# Lowest number to number before inner
		# If the two ranges shared a start point, then comb[1]-1 == comb[0]-1 
		# and lower[0] == lower[1] + 1. IE: there isn't anything below the inner
		# range after all. 
		if lower[0] < lower[1]:
			ret_ranges.append(lower)

	# Same logic in reverse for the range above the interior range: 
	if comb[-1] == xmas[-1]:
		upper = (comb[2] + 1, comb[3])
		if upper[0] < upper[1]:
			ret_ranges.append(upper)

	return (True, ret_ranges)


def do_part_two_for(lines):

	graph = {}
	for defn in lines:
		# This time, we're *only* processing the workflow strings. 
		if defn == "":
			break

		wf_name, wf_body = defn.split("{")
		wf_rule_defs = wf_body[:-1].split(",")
		for i, rule_def in enumerate(wf_rule_defs):
			graph_node(wf_name, i, rule_def, graph)
	
	xmas_tuples = {id: (1, 4000) for id in "xmas"}
	all_possibilities = 4000 ** 4
	accepted = 0
	process_queue = deque([(("in", 0), xmas_tuples, all_possibilities)])
	while process_queue:
		node_address, xmas, possibilities = process_queue.popleft()
		if node_address == ("A", 0):
			accepted += possibilities
			continue
		elif node_address == ("R", 0):
			continue

		node = graph[node_address]
		node: graph_node

		xmas_range = xmas[node.checked_id]
		scope = xmas_range[1] - xmas_range[0] + 1
		per_capita = possibilities // scope
		node_range = (node.lower, node.upper)
		intersected, out_ranges = split_ranges(node_range, xmas_range)
		
		sanity = 0
		if intersected:
			this_range = out_ranges.pop(0)
			new_scope = this_range[1] - this_range[0] + 1
			new_possibilities = per_capita * new_scope
			sanity += new_possibilities
			new_xmas = xmas.copy() 
			new_xmas[node.checked_id] = this_range
			process_queue.append((node.dest_true, new_xmas, new_possibilities))
		
		for rem_out_range in out_ranges:
			new_scope = rem_out_range[1] - rem_out_range[0] + 1
			new_possibilities = per_capita * new_scope
			sanity += new_possibilities
			new_xmas = xmas.copy()
			new_xmas[node.checked_id] = rem_out_range
			process_queue.append((node.dest_false, new_xmas, new_possibilities))

		if sanity != possibilities:
			raise ArithmeticError("Andrew's arithmetic was bad")

	return accepted
		

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"Given a list of workflows, we need to sort a list of parts into bin"
	   	  f"s that are either ""Accepted"" or ""Rejected"" and then output the "
		  f"sum of the ratings for all parts in the ""Accepted"" bin.\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe sum of the ratings is {results}")
	print(f"\tWe expected: 19114\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe sum of the ratings is {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"How many distinct combinations of ratings will be accepted?\n")

	results = do_part_two_for(example_lines)
	print(f"When we do part two for the example input:")
	print(f"\tThe number of distinct combinations of ratings that will be accep"
		  f"ted is {results}")
	print(f"\tWe expected: 167409079868000\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe number of distinct combinations of ratings that will be accep"
		  f"ted is {results}\n")

def print_header():
	print("--- DAY 19: Aplenty ---\n")
