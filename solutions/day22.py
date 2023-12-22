# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

import itertools
from functools import lru_cache
import sys

try:
	input_lines = io.read_input_as_lines(22)
	example_lines = io.read_example_as_lines(22)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]

def tween(tup1, tup2):
	tmin = (min(tup1[0], tup2[0]), min(tup1[1], tup2[1]), min(tup1[2], tup2[2]))
	tmax = (max(tup1[0], tup2[0]) + 1, max(tup1[1], tup2[1]) + 1, 
	 		max(tup1[2], tup2[2]) + 1)
	xs = [tmin[0]] + [x for x in range(tmin[0] + 1, tmax[0])]
	ys = [tmin[1]] + [y for y in range(tmin[1] + 1, tmax[1])]
	zs = [tmin[2]] + [z for z in range(tmin[2] + 1, tmax[2])]
	xyzs = [xyz for xyz in itertools.product(xs, ys, zs)]
	return xyzs

def do_part_one_for(lines, debug=False):
	BRICK_IND = 0
	cube_space = defaultdict(lambda: -1)
	bricks = {}
	for line in lines:
		beg, end = line.split("~")
		beg = tuple([int(n) for n in beg.split(",")])
		end = tuple([int(n) for n in end.split(",")])
		brick_cubes = tween(beg, end)
		for c in brick_cubes:
			cube_space[c] = BRICK_IND
		bricks[BRICK_IND] = brick_cubes
		BRICK_IND += 1

	# We need to process bricks from the lowest brick to the highest brick.
	def bottom_z(brick_cube_ind):
		brick_cubes = bricks[brick_cube_ind]
		return min(c[2] for c in brick_cubes)
	asc_brick_ids = sorted(bricks.keys(), key=bottom_z)

	# Iteratively drop bricks starting with the lowest brick in the space until
	# all bricks have come to a rest. 
	def drop_one(cube_v):
		return (cube_v[0], cube_v[1], cube_v[2]-1)
	def can_drop(cube_v):
		return cube_space[drop_one(cube_v)] in (-1, cube_space[cube_v])
	for bid in asc_brick_ids:
		brick = bricks[bid]
		brick_z = bottom_z(bid)
		while brick_z > 1 and all(can_drop(v) for v in brick):
			new_brick = []
			for c in brick:
				c_dropped = drop_one(c)
				cube_space[c_dropped] = cube_space[c]
				cube_space[c] = -1 
				new_brick.append(c_dropped)
			bricks[bid] = new_brick
			brick = new_brick
			brick_z -= 1
	
	# All the bricks are at rest. Which ones are supporting which other ones? 
	elligibles = set(asc_brick_ids.copy())
	for brick_id in asc_brick_ids:
		below = set([cube_space[drop_one(c)] for c in bricks[brick_id]])
		below = list([bid for bid in below if bid not in (-1, brick_id)])
		brick_nm = f"Brick {chr(brick_id+65)}"
		below_nms = [chr(b+65) for b in below]

		if debug:
			print(f"{brick_nm} rests on {len(below)} brick(s): {below_nms}")
		if len(below) == 1:
			below_nm = f"Brick {chr(below[0]+65)}"
			if below[0] in elligibles:
				if debug:
					print(f"Since {below_nm} is {brick_nm}'s only support, it c"
	  					  f"annot be removed!")
				elligibles.remove(below[0])
			elif debug: 
				print(f"{below_nm} is the only support for {brick_nm}, too!")
	if debug:
		print(f"\nThus, the only bricks that *can* be disintegrated are:")
		for e in elligibles:
			print(f"\t- Brick {chr(e+65)}")
		print()
	return len(elligibles)

class BrickNode:

	REGISTRY = {}

	@staticmethod
	def get(id):
		return BrickNode.REGISTRY[id]

	def __init__(self, brick_id) -> None:
		self.brick_id = brick_id
		self.supports = []
		self.supported_by = []
		self.bricks_i_dropped = set()
		BrickNode.REGISTRY[brick_id] = self
		self.repr = ""

	def provide_support(self, above_id):
		if above_id == self.brick_id:
			return
		self.supports.append(BrickNode.REGISTRY[above_id])
		BrickNode.REGISTRY[above_id].supported_by.append(self)
	
	def collapse_count(self, supports_affected=None, dropped=None):
		# Initial entry: this brick doesn't count because it was disintegrated,
		# but all the bricks above it have at least one less support. Propogate
		# the missing/falling bricks up:
		if supports_affected == None:
			sup_set = set([self]).union(set(self.supports))
			dropped = set([self])
			counts = [n.collapse_count(sup_set, dropped) for n in self.supports]
			return 0 + sum(counts)
		
		# Subsequent entries: We've lost at least one support. Check if we've 
		# lost all supports:
		baseline_supports = set(self.supported_by)
		remaining_supports = baseline_supports.difference(supports_affected)

		# If we're still supported or if we already dropped, then don't "drop 
		# again" and increase the count 
		if remaining_supports:
			return 0
		
		if self in dropped:
			return 0
		
		# But if we no longer have any supports, we do drop and we stop 
		# supporting anything that's above us. 
		else:
			summation = 1 
			supports_affected = supports_affected.union(set(self.supports))
			dropped.add(self)
			for n in self.supports:
				summation += n.collapse_count(supports_affected, dropped)
			return summation
	
	def __eq__(self, __value: object) -> bool:
		self.brick_id == __value.brick_id

	def __hash__(self) -> int:
		return hash(self.brick_id)

	def __repr__(self) -> str:
		if self.repr == "":
			id_remaining = self.brick_id
			while id_remaining > 25:
				self.repr = chr(id_remaining % 26 + 65) + self.repr
				id_remaining -= (id_remaining % 26)
				id_remaining //= 26
			self.repr = f"Brick {chr(id_remaining + 65)}{self.repr}"
		return self.repr
			


def do_part_two_for(lines):
	# Recursion limit is lower than the input set length, but if one 
	# lode-bearing node would cause the whole thing to collapse then it would 
	# need to recurse through the whole set
	sys.setrecursionlimit(1270)

	BRICK_IND = 0
	cube_space = defaultdict(lambda: -1)
	bricks = {}
	for line in lines:
		beg, end = line.split("~")
		beg = tuple([int(n) for n in beg.split(",")])
		end = tuple([int(n) for n in end.split(",")])
		brick_cubes = tween(beg, end)
		for c in brick_cubes:
			cube_space[c] = BRICK_IND
		bricks[BRICK_IND] = brick_cubes
		BrickNode(BRICK_IND)
		BRICK_IND += 1

	# We need to process bricks from the lowest brick to the highest brick.
	def bottom_z(brick_cube_ind):
		brick_cubes = bricks[brick_cube_ind]
		return min(c[2] for c in brick_cubes)
	asc_brick_ids = sorted(bricks.keys(), key=bottom_z)

	# Iteratively drop bricks starting with the lowest brick in the space until
	# all bricks have come to a rest. 
	def drop_one(cube_v):
		return (cube_v[0], cube_v[1], cube_v[2]-1)
	def can_drop(cube_v):
		return cube_space[drop_one(cube_v)] in (-1, cube_space[cube_v])
	for bid in asc_brick_ids:
		brick = bricks[bid]
		brick_z = bottom_z(bid)
		while brick_z > 1 and all(can_drop(v) for v in brick):
			new_brick = []
			for c in brick:
				c_dropped = drop_one(c)
				cube_space[c_dropped] = cube_space[c]
				cube_space[c] = -1 
				new_brick.append(c_dropped)
			bricks[bid] = new_brick
			brick = new_brick
			brick_z -= 1
		
		bricks_below = set([cube_space[drop_one(c)] for c in brick])
		for below_id in bricks_below:
			if below_id == -1:
				continue
			BrickNode.get(below_id).provide_support(bid)
	
	for first_brick in asc_brick_ids:
		supports = {b: BrickNode.get(b).supported_by for b in range(BRICK_IND)}
		supports = {b: set(supports[b]) for b in supports.keys()}

		last_unsupported_count = -1
		unsupported = set()
		disturbed = set()
		while len(unsupported) != last_unsupported_count:
			last_unsupported_count = len(unsupported)
			



	
	#return sum([BrickNode.get(b).collapse_count() for b in range(BRICK_IND)])

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"Simulate the falling of a series of bricks, and then after they've "
       	  f"settled, return the count of bricks that can be safely disintegrate"
		  f"d without causing the bricks above to fall.\n")

	print(f"When we do part one for the example input:")
	results = do_part_one_for(example_lines, True)
	print(f"\tThe count of disintegratable bricks is {results}")
	print(f"\tWe expected: 5\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe count of disintegratable bricks is {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"For each brick that you disintegrate, a number of bricks would fall"
       	  f". What is the sum of that number for each brick in the stack?\n")

	results = do_part_two_for(example_lines)
	print(f"When we do part two for the example input:")
	print(f"\tThe sum of rocks that would fall if you disintegrated each is {results}")
	print(f"\tWe expected: 7\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe <THING THEY WANT> is {results}\n")

def print_header():
	print("--- DAY 22: <TITLE GOES HERE> ---\n")
