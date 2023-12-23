# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

from itertools import product

try:
	input_lines = io.read_input_as_lines(22)
	example_lines = io.read_example_as_lines(22)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]

class Brick:

	BRICKS_MADE: int = 0
	REGISTRY: 'dict[int, Brick]' = {} 
	WORLD: 'dict[tuple[int], int]' = defaultdict(lambda: -1)

	SAVED_REGISTRY: 'dict[int, Brick]' = {} 
	SAVED_WORLD: 'dict[tuple[int], int]' = defaultdict(lambda: -1)

	@staticmethod
	def get(index: int) -> 'Brick':
		return Brick.REGISTRY[index]
		
	@staticmethod
	def register(brick: 'Brick') -> None:
		brick.id = Brick.BRICKS_MADE
		Brick.BRICKS_MADE += 1
		Brick.REGISTRY[brick.id] = brick

	@staticmethod
	def drop_all() -> int:
		bricks = Brick.REGISTRY
		brick_ids = sorted(bricks.keys(), key=lambda b:Brick.get(b).z_min())
		moved = set()
		for bid in brick_ids:
			b = bricks[bid]
			while not b.below() and b.z_min() > 1:
				moved.add(b.id)
				b.drop()
		return len(moved)

	@staticmethod
	def reset() -> None:
		Brick.REGISTRY = {}
		Brick.BRICKS_MADE = 0
		Brick.WORLD = defaultdict(lambda: -1)

	@staticmethod
	def save_state_static() -> None:
		Brick.SAVED_REGISTRY = Brick.REGISTRY.copy()
		for brick in Brick.SAVED_REGISTRY.values():
			brick.save_state()
		Brick.SAVED_WORLD = defaultdict(lambda: -1)
		for k, v in list(Brick.WORLD.items()):
			if v == -1:
				continue
			Brick.SAVED_WORLD[k] = v
	
	@staticmethod
	def restore_save_state_static() -> None:
		Brick.REGISTRY = Brick.SAVED_REGISTRY.copy()
		Brick.WORLD = Brick.SAVED_WORLD.copy()
		for brick in Brick.REGISTRY.values():
			brick.restore_save_state()

	def __init__(self, def_str) -> None:
		self.id = Brick.BRICKS_MADE
		s, e = [[int(n) for n in v.split(",")] for v in def_str.split("~")]
		self.components = tween(s, e)
		Brick.register(self)
		for c in self.components:
			Brick.WORLD[c] = self.id
	
	def z_min(self) -> int:
		return min(c[2] for c in self.components)

	def above(self) -> 'list[int]':
		brick_ids_above = []
		for c in self.components:
			above_c = (c[0], c[1], c[2] + 1)
			if Brick.WORLD[above_c] not in (-1, self.id):
				brick_ids_above.append(Brick.WORLD[above_c])
		return set(brick_ids_above)

	def below(self) -> 'list[int]':
		brick_ids_below = []
		for c in self.components:
			below_c = (c[0], c[1], c[2] - 1)
			if Brick.WORLD[below_c] not in (-1, self.id):
				brick_ids_below.append(Brick.WORLD[below_c])
		return set(brick_ids_below)
	
	def disintegrate(self) -> None:
		for c in self.components:
			Brick.WORLD[c] = -1
		Brick.REGISTRY.pop(self.id)
	
	def drop_distance(self):
		actual_steps = 999999
		for c in self.components:
			x, y, z = c
			probe_steps = 0
			probe_z = z
			while probe_z > 1 and Brick.WORLD[(x, y, probe_z)] in (-1, self.id):
				probe_steps += 1
				probe_z -= 1
				if probe_z == actual_steps:
					break
			actual_steps = min(actual_steps, probe_steps)
		return actual_steps

	def drop(self):
		dist = self.drop_distance()
		fish = "No"
		for index, coord in enumerate(self.components.copy()):
			Brick.WORLD[coord] = -1
			new_coord = (coord[0], coord[1], coord[2] - 1)
			self.components[index] = new_coord
			Brick.WORLD[new_coord] = self.id

	def save_state(self):
		self.saved_components = self.components.copy()

	def restore_save_state(self):
		self.components = self.saved_components.copy()
		
	def __repr__(self) -> str:
		return chr(self.id + 65)

def tween(tup1, tup2):
	tmin = (min(tup1[0], tup2[0]), min(tup1[1], tup2[1]), min(tup1[2], tup2[2]))
	tmax = (max(tup1[0], tup2[0]), max(tup1[1], tup2[1]), max(tup1[2], tup2[2]))
	xs = [tmin[0]] + [x for x in range(tmin[0] + 1, tmax[0] + 1)]
	ys = [tmin[1]] + [y for y in range(tmin[1] + 1, tmax[1] + 1)]
	zs = [tmin[2]] + [z for z in range(tmin[2] + 1, tmax[2] + 1)]
	xyzs = [xyz for xyz in product(xs, ys, zs)]
	return xyzs

def do_part_one_for(lines, debug=False):
	Brick.reset()
	for ln in lines:
		Brick(ln)

	Brick.drop_all()

	safe = 0
	for lower in range(len(lines)):
		lower_brick = Brick.get(lower)
		uppers = Brick.get(lower).above()
		all_supported = True
		for upper in uppers:
			upper_brick = Brick.get(upper)
			upper_supports = upper_brick.below()
			all_supported = all_supported and len(upper_supports) != 1
		safe += 1 if all_supported else 0
	return safe


def do_part_two_for(lines):
	Brick.reset()
	for ln in lines:
		Brick(ln)
	Brick.drop_all()
	Brick.save_state_static()

	total_moved = 0
	for to_disintegrate in range(len(lines)):
		Brick.restore_save_state_static()
		Brick.get(to_disintegrate).disintegrate()
		total_moved += Brick.drop_all()
	return total_moved


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
