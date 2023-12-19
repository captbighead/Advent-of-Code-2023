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

class tree_node:

	def __init__(self) -> None:
		
		# Make a tree, of the decisions, take 4 tuples (0:4000) inclusive, bring
		# them down through the tree until they reach a leaf node. For every 
		# leaf node: mutiply the cardinalities of the tuples against each other
		# to get that leaf node's possibility space. Multiply the leaf nodes' 
		# spaces together, bada bing bada boom 


def do_part_two_for(lines):
	for defn in lines:
		# This time, we're *only* processing the workflow strings. 
		if defn == "":
			break

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
	print("--- DAY 19: <TITLE GOES HERE> ---\n")
