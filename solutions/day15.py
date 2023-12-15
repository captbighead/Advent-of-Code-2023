# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

try:
	input_lines = io.read_input_as_lines(15)
except:
	input_lines = ["Input Lines Not Found"]

example_lines = ["rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"]

def not_an_actual_hash(input_str):
	current_value = 0
	for c in input_str:
		current_value += ord(c)
		current_value *= 17
		current_value %= 256
	return current_value
	

def do_part_one_for(lines):
	summation = 0
	for seq_val in lines[0].split(","):
		summation += not_an_actual_hash(seq_val)
	return summation

def do_part_two_for(lines):
	boxes = [{"bottom": 0} for i in range(256)]
	sequence = lines[0].split(",")
	for token in sequence:
		# Equals operation
		if token.find("=") + 1:
			label, focal_length = token.split("=")
			focal_length = int(focal_length)
			
			# The box is a dict, storing lenses as a 2-element list of their 
			# ordering within the box and their focal length. The left element 
			# is the ordering, and it's zero-indexed from top to bottom. The box
			# also remembers the index at its bottom. 
			#
			# The ordering values will not be contiguous, but they will be 
			# ordered
			label_hash = not_an_actual_hash(label) 
			box = boxes[label_hash]
			bottom = box["bottom"]

			# If there is no lens with the label in the box, put it on the 
			# bottom of the box.
			if not box.get(label, False):
				box[label] = [bottom, focal_length]
				box["bottom"] += 1
			
			# If there is a lens with that label already in the box, replace the
			# previous lens with the new one in the same place in the stack. 
			else:
				box[label][1] = focal_length

		# Dash operation - we remove a lens of a given label. Technically, 
		# everything else is supposed to shuffle forward, but everything is 
		# still in the same order so we won't bog down the process by doing that
		else:
			label = token[:-1]
			label_hash = not_an_actual_hash(label)
			try:
				boxes[label_hash].pop(label)
			except KeyError:
				pass	# If it's not in there then that's fine. 
	
	# Now we calculate the focusing power:
	focusing_power = 0
	for box_id, box in enumerate(boxes, 1):
		box.pop("bottom")	# This is gonna make everything all weird
		lenses = [t[1] for t in sorted([v for v in box.values()])]

		pass
		for i, focal_length in enumerate(lenses, 1):
			focusing_power += box_id * i * focal_length
	return focusing_power


			



def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"For part one, we're testing out a hashing function by returning the"
       	  f" sum of the hashes of the instructions.\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe sum of the hash values is {results}")
	print(f"\tWe expected: 1320\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe sum of the hash values is {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"Now we need to arrange and sort a series of lenses based on the ins"
       	  f"tructions.\n")

	results = do_part_two_for(example_lines)
	print(f"When we do part two for the example input:")
	print(f"\tThe focusing power of the lenses is {results}")
	print(f"\tWe expected: 145\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe focusing power of the lenses is {results}\n")

def print_header():
	print("--- DAY 15: Lens Library ---\n")
