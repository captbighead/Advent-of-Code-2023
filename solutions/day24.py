# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

try:
	input_lines = io.read_input_as_lines(24)
	example_lines = io.read_example_as_lines(24)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]

MAX_X = 1
MAX_Y = 1

class BlizzardValley:

	class Blizzard:

		def __init__(self, position, bearing) -> None:
			self.start = position
			self.position = position
			self.direction = bearing
			self.axis = "y" if bearing in (vector.UP(), vector.DOWN()) else "x"

		def move(self):
			unclamped = self.position + self.direction
			self.position = vector(unclamped.x % MAX_X, unclamped.y % MAX_Y)
			return self.position == self.start
				

	def __init__(self, init_vs: dict[vector, str]) -> None:
		DIRS = {
			">": vector.RIGHT(),
			"<": vector.LEFT(),
			"^": vector.UP(),
			"v": vector.DOWN(),
		}
		
		blizzards = []
		for b in init_vs.keys():
			if init_vs[b] != ".":
				blizzards.append(BlizzardValley.Blizzard(b, DIRS[init_vs[b]]))
		
		x_set = set(x for x in range(MAX_X))
		y_set = set(y for y in range(MAX_Y))
		valley = {}
		for k in init_vs.keys():
			valley[k] = {"x": x_set.copy(), "y": y_set.copy()}
		
		# We're already on tick 0, so we need to do a quick check before we 
		# start moving any blizzards
		for b in blizzards:
			b: BlizzardValley.Blizzard
			valley[b.start][b.axis].remove(0)


		for t in range(max(MAX_X, MAX_Y)):
			removals = []
			for b in blizzards:
				b: BlizzardValley.Blizzard
				


		

		




	
	def position_at_tick(self, tick):
		travelled = self.dir * tick
		unadj = self.position + travelled
		unadj.x 
		return self.position + (scalar * self.dir)


def simulate_storm(valley_map, storms):
	pass

def do_part_one_for(lines):
	global MAX_X, MAX_Y
	MAX_X = len(lines[0]) - 2
	MAX_Y = len(lines) - 2

	blizzard_space = [ln[1:-1] for ln in lines[1:-1]]
	blizzard_space = algos.vector_map_from_string_list(blizzard_space)
	valley = BlizzardValley(blizzard_space)

def do_part_two_for(lines):
	pass

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"This is the prompt for Part One of the problem.\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe number of steps through the valley while dodging blizzards is"
		  f" {results}")
	print(f"\tWe expected: 18\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe number of steps through the valley while dodging blizzards is"
		  f" {results}\n")

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
