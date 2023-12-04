# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

try:
	input_lines = io.read_input_as_lines(4)
	example_lines = io.read_example_as_lines(4)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]

class scratchcard:

	def __init__(self, def_str, max_id) -> None:
		# Consecutive spaces screw with the split function
		while len(def_str.replace("  ", " ")) != len(def_str):
			def_str = def_str.replace("  ", " ")

		id_str, set_strs = def_str.split(": ")
		id = int(id_str.replace("Card ", ""))
		self.id = id
		wins, elfs = set_strs.split(" | ")
		self.card_wins = set([int(n) for n in wins.split(" ")])
		self.card_nums = set([int(n) for n in elfs.split(" ")])
		self.win_nums = self.card_wins.intersection(self.card_nums)
		wins = len(self.win_nums)
		self.points = 0 if not self.win_nums else 2 ** (wins - 1)
		self.awarded = [id + n + 1 for n in range(wins) if id + n + 1 <= max_id]

def do_part_one_for(lines):
	return sum(scratchcard(ln, len(lines)).points for ln in lines)

def do_part_two_for(lines):
	scratchcards = [scratchcard(ln, len(lines)) for ln in lines]
	scratchcards = {sc.id: sc.awarded for sc in scratchcards}
	duplicates = {k: 1 for k in scratchcards.keys()}
	for i in range(1, len(lines) + 1):
		for a in scratchcards[i]:
			duplicates[a] += duplicates[i]
	return sum(duplicates.values())

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"This is the prompt for Part One of the problem.\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe <THING THEY WANT> is {results}")
	print(f"\tWe expected: <SOLUTION THEY WANT>\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe <THING THEY WANT> is {results}\n")

def solve_p2():
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
	print("--- DAY 4: <TITLE GOES HERE> ---\n")
