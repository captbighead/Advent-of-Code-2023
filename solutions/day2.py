# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

try:
	input_lines = io.read_input_as_lines(2)
	example_lines = io.read_example_as_lines(2)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]

def empty_round_factory():
	return {"red": 0, "green": 0, "blue": 0}

def parse_games_from_lines(lines):
	games_by_id = {}
	for line in lines:
		header, round_str = line.split(": ")
		id = int(header.replace("Game ", ""))
		rounds = []
		round_defs = round_str.split("; ")
		for rdef in round_defs:
			round = empty_round_factory()
			tokens = rdef.split(", ")
			for token in tokens:
				num, colour = token.split(" ")
				round[colour] = int(num)
			rounds.append(round)
		games_by_id[id] = rounds
	return games_by_id

   
def do_part_one_for(lines):
	# Verify that each game is possible, given these facts. 
	FACTS = {"red": 12, "green": 13, "blue": 14}
	
	# Go through each game and check it against the facts for part one. 
	elf_games = parse_games_from_lines(lines)
	running_sum = 0
	for game_id in elf_games.keys():
		game_is_legal = True
		for round in elf_games[game_id]:
			for colour in FACTS.keys():
				game_is_legal = game_is_legal and round[colour] <= FACTS[colour]
		
		running_sum += game_id if game_is_legal else 0
	
	return running_sum
		

def do_part_two_for(lines):
	# This time we want to return the set of facts that allows each game to be 
	# possible. 
	sum_of_powers = 0
	elf_games = parse_games_from_lines(lines)
	for game_id in elf_games.keys():
		facts = empty_round_factory()
		for round in elf_games[game_id]:
			for colour in round.keys():
				facts[colour] = max(round[colour], facts[colour])
		power = facts["red"] * facts["green"] * facts["blue"]
		sum_of_powers += power
	return sum_of_powers


def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"A lonely elf wants to play a 'game' with us. First, he's going to d"
		  f"escribe a series of these games to us and we need to determine if t"
		  f"hey are possible if the bag contained only 12 red cubes, 13 green c"
		  f"ubes, and 14 blue cubes\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe sum of game ids that were legal for the facts gives is "
		  f"{results}")
	print(f"\tWe expected: 8\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe sum of game ids that were legal for the facts gives is "
		  f"{results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"Now he wants to know the fewest number of cubes of each colour wher"
	   	  f"e the games would have been possible. He calls the product of those"
		  f" numbers the power, and wants us to find the sum of the powers for "
		  f"the given games.\n")

	results = do_part_two_for(example_lines)
	print(f"When we do part two for the example input:")
	print(f"\tThe sum of the powers is {results}")
	print(f"\tWe expected: 2286\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe sum of the powers is {results}\n")

def print_header():
	print("--- DAY 2: Cube Conundrum ---\n")
