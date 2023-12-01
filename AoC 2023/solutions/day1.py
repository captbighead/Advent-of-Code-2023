# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

try:
	input_lines = io.read_input_as_lines(1)
except:
	input_lines = ["Input Lines Not Found"]

example_lines = ["1abc2", "pqr3stu8vwx", "a1b2c3d4e5f", "treb7uchet"]
example_lines_2 = [
	"two1nine", "eightwothree", "abcone2threexyz", "xtwone3four", 
	"4nineeightseven2", "zoneight234", "7pqrstsixteen"
]

def do_part_one_for(lines):
	sum = 0
	for ln in lines:
		digits = [int(c) for c in ln if c.isnumeric()]
		sum += digits[0] * 10 + digits[-1]
	return sum

def do_part_two_for(lines):
	digital_lookup = {
		"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, 
		"six": 6, "seven": 7, "eight": 8, "nine": 9
	}

	def first_digit(word):
		for i, c in enumerate(word):
			if c.isnumeric():
				return int(c)
			
			# Check if the alphabetic character is part of a spelled out digit:
			for l in range(3, 6):
				if word[i:i+l] in digital_lookup.keys():
					return digital_lookup[word[i:i+l]]
	
	def last_digit(word):
		# We need to do the same logic, but from the back of the word. 
		rev_word = "".join(reversed(word))
		for i, c in enumerate(rev_word):
			if c.isnumeric():
				return int(c)
			
			# Check if the alphabetic character is part of a spelled out digit, 
			# but remember that the word is backwards:
			for l in range(3, 6):
				sub_word = "".join(reversed(rev_word[i:i+l]))
				if sub_word in digital_lookup.keys():
					return digital_lookup[sub_word]

	sum = 0
	for line in lines:
		sum += first_digit(line) * 10 + last_digit(line)
	return sum

	

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"We've been loaded into a trebuchet, but some elf's kid went and dre"
       	  f"w on the calibration checklist. There are numbers on lines in the c"
		  f"hecklist: report the sum of two-digit numbers generated from the fi"
		  f"rst and last digits on each line.\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe sum of the calibration values is {results}")
	print(f"\tWe expected: 142\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe sum of the calibration values is {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"Second verse same as the first, except some digits are spelled!\n")

	results = do_part_two_for(example_lines_2)
	print(f"When we do part two for the example input:")
	print(f"\tThe sum of the calibration values is {results}")
	print(f"\tWe expected: 281\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe sum of the calibration values is {results}\n")

def print_header():
	print("--- DAY 1: Trebuchet?! ---\n")
