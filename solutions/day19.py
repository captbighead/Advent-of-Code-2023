# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

import copy
import math

try:
	input_lines = io.read_input_as_lines(19)
	example_lines = io.read_example_as_lines(19)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]

RESOURCES = ["ORE", "CLAY", "OBSIDIAN", "GEODE"]
RES_TYPES = ["STOCK", "BOTS"]
PRINT_DEBUG_MSGS = True	# False

class search_state:

	def __init__(self, blueprint: dict, parent=None) -> None:
		cloning = isinstance(parent, search_state)
		if cloning: 
			self.time = parent.time
			self.state = copy.deepcopy(parent.state)
			self.ready_for_geodes = parent.ready_for_geodes
			self.ready_for_obsidian = parent.ready_for_obsidian
		else: 
			self.time = 0
			self.state = {}
			for r in RESOURCES:
				self.state[r] = {t: 0 for t in RES_TYPES}
			self.state["ORE"]["BOTS"] = 1
			self.ready_for_geodes = False
			self.ready_for_obsidian = False
		self.blueprint = blueprint
		self.hashval = None

	def time_to_next(self, resource):
		# Return a time that is out of scope if we're barking up the wrong tree
		if resource == "OBSIDIAN" and not self.ready_for_obsidian:
			return 25
		if resource == "GEODE" and not self.ready_for_geodes:
			return 25

		time_to_next = 1		# At least one minute
		for req in self.blueprint[resource].keys():
			stock = self.state[req]["STOCK"]
			quota = self.blueprint[resource][req]
			if stock >= quota:
				time_to_next = max(time_to_next, 1)
			else:
				deficit = quota - stock
				cycles = math.ceil(deficit / self.state[req]["BOTS"])
				time_to_next = max(time_to_next, 1 + cycles)
		return time_to_next


	def next_states(self) -> list:
		child_states = []

		# If time is 23, then even if we have a stockpile that lets us build any
		# robot, even a geode bot, it is created at the time limit so it's 
		# useless. 
		if self.time >= 23:
			return []

		for resource in RESOURCES:
			# If we have bots equal to the maximum cost of that resource in the
			# blueprint, having more is redundant. 
			if self.state[resource]["BOTS"] == self.blueprint["MAX"][resource]:
				continue

			# Similarly, if we don't have any clay bots, don't consider making
			# an obsidian bot (we can't)
			if resource == "OBSIDIAN" and not self.ready_for_obsidian:
				continue

			# Ditto for obsidian bots and geodes.
			if resource == "GEODE" and not self.ready_for_geodes:
				continue

			# If making this resource would take us past our time limit, then we
			# can't do it. If it's 23
			time_to_next = self.time_to_next(resource)
			time_at_next = time_to_next + self.time
			if time_at_next > 23:
				continue

			# After all that pruning, if we're still here, then making a new bot
			# for this resource might pay dividends.
			child_state = search_state(self.blueprint, self)
			child_state.time = time_at_next
			for child_resource in RESOURCES:
				cr_cost = self.blueprint[resource].get(child_resource, 0)
				cr_prod = self.state[child_resource]["BOTS"]
				cr_delta = cr_prod * time_to_next - cr_cost
				child_state.state[child_resource]["STOCK"] += cr_delta

				if child_state.state[child_resource]["STOCK"] < 0:
					print("WAIT UP")

			child_state.state[resource]["BOTS"] += 1

			# Rather than a verbose lookup, just update a flag if necesessary
			if resource == "CLAY":
				child_state.ready_for_obsidian = True
			elif resource == "OBSIDIAN":
				child_state.ready_for_geodes = True

			child_states.append(child_state)

		return child_states
	
	def __hash__(self) -> int:
		if self.hashval == None:
			vals = [self.state[r][t] for r in RESOURCES for t in RES_TYPES]
			vals.append(self.time)
			self.hashval = hash(tuple(vals))
		return self.hashval
	
	def __eq__(self, __value: object) -> bool:
		same_class = isinstance(__value, search_state)
		if same_class:
			for r in RESOURCES:
				for t in RES_TYPES:
					if self.state[r][t] != __value.state[r][t]:
						return False
			return True
		return False


def parse_blueprints(bp_defs):
	blueprints = []
	for bp_def in bp_defs:
		# Restructure the string into the parts that matter:
		removals = ["Blueprint ", " robot costs", " Each ", "and "]
		bp_def = algos.erase(bp_def, removals).upper()
		id, bp_def = bp_def.split(":")
		bp_def = bp_def[:-1]	# Ignore trailing '.'

		# bp_def is now of the format: 
		# 	<RES_NAME> <NUM_RES_1> <RES_1_NAME>[ <NUM_RES_2> <RES_2_NAME>]
		# but seperated by '.'

		# Blueprints are dicts with lookups for their ID, as well as the costs
		# in raw resources to make. 
		bp = {"ID": int(id)}
		for recipe in bp_def.split("."):	
			recipe = recipe.split()
			
			# Strip the name of the primary resource out
			resource = recipe[0]
			recipe = recipe[1:]

			# Recipe is now one or two pairs of: <NUM> <NAME> such that when we
			# call bp[<RESOURCE>][<NAME>] we get the amount of the secondary 
			# resource we need: <NUM>
			bp[resource] = {}
			for i in range(0, len(recipe), 2):	
				bp[resource][recipe[i+1]] =  int(recipe[i])
		
		# Record the maximum values needed of each resource:
		bp["MAX"] = {
			"ORE": max([bp[r]["ORE"] for r in RESOURCES]),
			"CLAY": bp["OBSIDIAN"]["CLAY"],
			"OBSIDIAN": bp["GEODE"]["OBSIDIAN"],
			"GEODE": 301
		}

		blueprints.append(bp)

	return blueprints

def get_quality(blueprint):
	best_geode_counts = {n: 0 for n in range(25)}
	#def recursive_dfs()
	

def do_part_one_for(lines):
	pass

def do_part_two_for(lines):
	pass

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"This is actually a WIP implementation attempt of problem 19 from la"
	   	  f"st year.\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe sum of the qualities of the blueprints is {results}")
	print(f"\tWe expected: <SOLUTION THEY WANT>\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe sum of the qualities of the blueprints is {results}\n")

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
	print("--- DAY 19: <TITLE GOES HERE> ---\n")
