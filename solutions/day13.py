# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

try:
	input_lines = io.read_input_as_lines(13)
	example_lines = io.read_example_as_lines(13)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]

def rotato_potato(image_strs):
	rotato = [["0"] * len(image_strs) for n in range(len(image_strs[0]))]
	#x y => (leny - y) x
	modifier = len(image_strs) - 1
	for y in range(len(image_strs)):
		for x in range(len(image_strs[0])):
			rotato[x][modifier - y] = image_strs[y][x]
	for i, array in enumerate(rotato):
		rotato[i] = "".join(array)
	return rotato


def find_symmetry(image_strs):
	image_strs = image_strs.copy()

	# Try Horizontal first. 
	horiz_symm = 0
	for y in range(len(image_strs)-1):
		y_neg = y
		y_pos = y_neg + 1
		while image_strs[y_neg] == image_strs[y_pos]:
			y_neg -= 1
			y_pos += 1

			# Only gets to here if all the lines leading to it are equal
			if y_neg == -1 or y_pos == len(image_strs):
				horiz_symm =  100 * (y + 1)		# Cols/Rows are 1-indexed
				break
	
	# If we haven't returned, it's not horizontally symmetrical. So flip the 
	# horizontal and vertical axes and then do it again
	new_image_strs = rotato_potato(image_strs)

	# This is the 'do it again' part. y is what used to be x. 
	vert_symm = 0
	for y in range(len(new_image_strs)-1):
		y_neg = y
		y_pos = y_neg + 1
		while new_image_strs[y_neg] == new_image_strs[y_pos]:
			y_neg -= 1
			y_pos += 1

			# Only gets to here if all the lines leading to it are equal
			if y_neg == -1 or y_pos == len(new_image_strs):
				vert_symm = y + 1	# Col/Rows are 1-indexed for output
				break
	
	if vert_symm and horiz_symm:
		print("holupaminit")

	return vert_symm, horiz_symm

def fix_smudge(image_strs, old_symm_line):
	img = image_strs
	image_map = algos.vector_map_from_string_list(img)
	for y in range(len(img)):
		for x in range(len(img[0])):
			diff_v = vector(x, y)
			diff_char = "." if image_map[diff_v] == "#" else "#"

			test = [["0" for x in range(len(img[0]))] for y in range(len(img))]
			for v in image_map.keys():
				test[v.y][v.x] = diff_char if v == diff_v else image_map[v]
			test = ["".join(ln) for ln in test]

			try:
				test_symm_line = find_symmetry(test)
				if test_symm_line != old_symm_line:
					if test_symm_line[0] == old_symm_line[0]:
						return test_symm_line[1]
					else:
						return test_symm_line[0]
			except LookupError:
				pass

	raise LookupError("Couldn't find the smudge")



def do_part_one_for(lines):
	lines.append("")
	summation = 0
	sample = []
	for ln in lines:
		if ln != "":
			sample.append(ln)
		else:
			summation += max(find_symmetry(sample))
			sample = []
	return summation


def do_part_two_for(lines):
	if lines[-1] != "":
		lines.append("")
	summation = 0
	sample = []
	for ln in lines:
		if ln != "":
			sample.append(ln)
		else:
			symmetry_line = find_symmetry(sample)
			summation += fix_smudge(sample, symmetry_line)
			sample = []
	return summation

def solve_p1():
	print("Wuh-oh! Lost the solution for 13!\n")
	return

	print(f"PART ONE\n--------\n")
	print(f"This is the prompt for Part One of the problem.\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe <THING THEY WANT> is {results}")
	print(f"\tWe expected: 405\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe <THING THEY WANT> is {results}\n")

def solve_p2():
	print("Wuh-oh! Lost the solution for 13!\n")
	return

	print(f"PART TWO\n--------\n")
	print(f"This is the prompt for Part Two of the problem.\n")

	results = do_part_two_for(example_lines)
	print(f"When we do part two for the example input:")
	print(f"\tThe <THING THEY WANT> is {results}")
	print(f"\tWe expected: 400\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe <THING THEY WANT> is {results}\n")

def print_header():
	print("--- DAY 13: <TITLE GOES HERE> ---\n")
