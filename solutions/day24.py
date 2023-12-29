# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

from itertools import product

try:
	input_lines = io.read_input_as_lines(24)
	example_lines = io.read_example_as_lines(24)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]

def do_part_one_for(line_defs, is_example):
	MIN = 200000000000000 if not is_example else 7
	MAX = 400000000000000 if not is_example else 27

	def in_bounds(v):
		return v[0] >= MIN and v[0] <= MAX and v[1] >= MIN and v[1] <= MAX

	def generate_is_approaching_closure(x, y, m):
		# Assume P = (x, y) is on a line with slope m. This function returns a 
		# closure that takes a point v and returns true if that point is further
		# along the line from (x, y) (IE: v + nm = P, is n positive?)
		mx, my = m
		def is_approaching(v):
			vx, vy = v
			return vx < x if mx < 0 else vx > x and vy < y if my < 0 else vy > y
		return is_approaching

	lines = []
	approach_closures = []
	for line_def in line_defs:
		p, v = line_def.split(" @ ")
		p = tuple([int(n) for n in p.split(", ")[:2]])
		v = tuple([int(n) for n in v.split(", ")[:2]])
		m = v[1] / v[0]
		b = p[1] - m * p[0]
		lines.append((m, b))
		approach_closures.append(generate_is_approaching_closure(p[0], p[1], v))

	# Iterate over all of the intersections between the lines. Count += 1 if the
	# intersection is further along the line from both line's origins. 
	intersections = 0
	for ind_1, line_1 in enumerate(lines):
		for ind_2, line_2 in enumerate(lines[ind_1 + 1:], ind_1 + 1):
			
			# m_ is the slope of line_, b_ is the y-intercept of line_
			m1, b1 = line_1
			m2, b2 = line_2

			# Parallel lines don't cross
			if m1 == m2:
				continue

			# Did some algebra outside of the code and determined this is how
			# the intersection relates. 
			dm = (-m1) - (-m2)
			i = (((-b2) - (-b1)) / dm, (b1 * m2 - b2 * m1) / dm)

			line_1_approaching = approach_closures[ind_1](i) 
			line_2_approaching = approach_closures[ind_2](i)
			converging = line_1_approaching and line_2_approaching
			
			intersections += 1 if in_bounds(i) and converging else 0

	return intersections


def row_echelon_solver(matrix):
	def is_RREF(m):
		for i in range(len(m)):
			for j in range(len(m[i])):
				if i == j and m[i][j] == 1:	# RREF has i, i == 1
					continue
				elif j == len(m[i]) - 1:	# The final column is solns
					continue
				elif m[i][j]:				# All other cells must be 0 in RREF
					return False
		return True
	
	def swap_rows(m, i, j):
		buffer = m[i]
		m[i] = m[j]
		m[j] = buffer

	def divide_row_if_possible(m, r, n):
		if n == 0:
			return False
		
		divisible = True
		for v in m[r]:
			divisible = divisible and not v % n
		if not divisible:
			return False
		
		for i, v in enumerate(m[r]):
			m[r][i] = v // n
		return True

	def apply_reductions(m, i, n, j):
		"""Adds n * i to j"""
		for ind, v in enumerate(m[i]):
			m[j][ind] += n * v
	
	# Perform one of the three operations to get the whole shebang into RREF:
	#
	#	1) Swap two rows
	#	2) Multiply a row by a non-zero number
	# 	3) Add a multiple of one row to another.
	#
	# We're trying to make the leftmost column conform to RREF. So we'll choose
	# what to do in that context. 
	col = 0		# The column we're working on.
	rows = len(matrix)
	cols = len(matrix[0])
	while not is_RREF(matrix):

		if col == 4:
			col = 0

		for r, row in enumerate(matrix[col:]):
			if row[col] < 0:
				for i, v in enumerate(row):
					row[i] = -v

		# Check if the active column is settled:
		is_one = matrix[col][col] == 1
		zeroes = sum(1 if matrix[r][col] == 0 else 0 for r in range(rows))
		if is_one and zeroes == rows - 1:
			col += 1
			continue

		# It's not settled. If our leading number is not 1, it might be 0. If 
		# that's the case, we need to swap in a row that has a non-zero value in
		# this space. 
		if not is_one and matrix[col][col] == 0:
			# One of the rows below us works; a row above us can't. Choose a row
			# with a 1 in it if we can.
			best_row = -1
			for r in range(col + 1, rows):
				if matrix[r][col] != 0:
					best_row = r 

				# If we can slot a 1 in, do that for sure.
				if matrix[r][col] == 1:
					break
			
			# We know a best row has to exist:
			if best_row == -1:
				raise ValueError("Andrew is bad at math apparently")
			
			swap_rows(matrix, best_row, col)
			continue
				
		# If we get here, we didn't swap, so we're not 0. We may not be one 
		# though. If we aren't, check if we can evenly divide our row (we're 
		# trying to stay with integer values)
		if not is_one:
			v = matrix[col][col]
			if divide_row_if_possible(matrix, col, v):
				continue
		
		# If we got here and we're still not is_one, then we couldn't divide 
		# this row properly. Maybe one of the other rows fits the bill?
		if not is_one:
			did_divide = False
			for r in range(col + 1, rows):
				if divide_row_if_possible(matrix, r, matrix[r][col]):
					did_divide = True
					break

			# If we did divide a different row, it is the new candidate for RREF
			if did_divide:
				swap_rows(matrix, col, r)
				continue
		
		# If we're *still* not one and we get *here* then we couldn't make any
		# row into 1 for this column through division or swapping alone. All 
		# that we have left is to add some multiple of one row to another. 
		if not is_one:

			# Should be impossible, just covering my bases. 
			if zeroes == rows - 1:
				raise ValueError("Yup. Andrew failed to math properly.")

			non_zero_rows = [r for r in range(col, rows) if matrix[r][col]]
			performed_op = False
			for rind, r1 in enumerate(non_zero_rows):
				for r2 in non_zero_rows[rind + 1:]:
					r1_lead = matrix[r1][col]
					r2_lead = matrix[r2][col]

					to_reduce = None
					reduce_by = None
					reductions = None
					if abs(r1_lead % r2_lead) == 1:
						to_reduce = r1
						reduce_by = r2
						reductions = r1_lead // r2_lead
					elif abs(r2_lead % r1_lead) == 1:
						to_reduce = r2
						reduce_by = r1
						reductions = r2_lead // r1_lead
					
					if to_reduce == None:
						continue

					apply_reductions(matrix, reduce_by, -reductions, to_reduce)
					swap_rows(matrix, reduce_by, to_reduce)
					performed_op = True
					break

				if performed_op:
					break

			if performed_op:
				continue

			if matrix[col + 1][col] != 0:
				# We need to do *something* to reduce the leading edge. 
				bigger = max((col, col + 1), key=lambda r: matrix[r][col])
				lower = min((col, col + 1), key=lambda r: matrix[r][col])
				n = matrix[bigger][col] // matrix[lower][col]
				apply_reductions(matrix, lower, -n, bigger)
				if matrix[col][col] < matrix[col+1][col]:
					swap_rows(matrix, bigger, lower)
				continue
				
			smallest_divisor = min(abs(n) for n in matrix[col] if n != 0)
			saved = False
			for div in range(smallest_divisor, 1, -1):
				saved = divide_row_if_possible(matrix, col, div)
				if saved:
					break
			if saved:
				continue
			
		# If we're here and we haven't failed out, we're 1 in our lead position,
		# but some rows also have values in our lead position. Because we're 1,
		# we can obliterate them really easily!
		if is_one:
			non_zeroes = [r for r in range(rows) if matrix[r][col] if r != col]
			for r in non_zeroes:
				apply_reductions(matrix, col, -matrix[r][col], r)
			continue

		# If we get here, there's nothing more we can do. Carry on to the 
		# next column. 
		col += 1
		continue
	
	return [matrix[r][-1] for r in range(rows)]

def do_part_two_for(lines):
	hailstones = []
	for hail_def in lines:
		hail = tuple(int(n) for n in hail_def.replace(" @", ",").split(","))
		hailstones.append(hail)
	
	eqs = 4
	xy_matrix = []
	zy_matrix = []

	for hail_a, hail_b in product(hailstones, repeat=2):
		if hail_a == hail_b:
			continue
		x, y, z, a, b, c = hail_a
		u, v, w, d, e, f = hail_b

		# Solves X, Y
		xy_matrix.append([e-b, a-d, y-v, u-x, e*u - d*v - b*x + a*y])

		# Solves Y, Z
		zy_matrix.append([e-b, c-f, y-v, w-z, e*w - f*v - b*z + c*y])

		eqs -= 1
		if not eqs:
			break

	X, Y, A, B = row_echelon_solver(xy_matrix)
	Z, Y, C, B = row_echelon_solver(zy_matrix)
	rock_pos = tuple([round(v) for v in (X, Y, Z)])
	rock_vel = tuple([round(v) for v in (A, B, C)])
	print(f"We've found X, Y, Z, and A, B, C: {rock_pos} and {rock_vel}")
	return sum(rock_pos)



		




#def do_part_two_for_numpy(lines):
#	# So, I *did* code this independently and did the math by myself, but it was
#	# following someone else's solution/instructions and checking my math 
#	# against theirs. It's been a long time since my linear algebra course...
#	#
#	#	Let Rock Position = X, Y, Z		Let Hailstone i Position = x, y, z
#	#	Let Rock Velocity = A, B, C		Let Hailstone i Velocity = a, b, c
#	#	
#	#	At some time t, the new Rock Position is:
#	#
#	#		X + tA, Y + tB, Z + tC
#	#
#	#	And it intersects with some hailstone: 
#	#
#	#		x + ta, y + tb, z + tc
#	#
#	#	Using the x positions we can find an equation for t:
#	#
#	#		X + tA = x + ta
#	#		X + tA - x = ta
#	#		X - x = ta - tA
#	#		X - x = t(a - A)
#	#		t = (X - x)/(a - A)
#	#
#	#	And the same holds for y, z:
#	#
#	#		t = (Y - y)/(b - B), (Z - z)/(c - C)
#	#
#	#	So we know t in terms of x, y, so we can express an equality entirely in
#	# 	terms of x, y:
#	#
#	#		(X - x)/(a - A) = (Y - y)/(b - B)
#	#		(b - B)(X - x) = (a - A)(Y - y)
#	#		bX - bx - BX + Bx = aY - ay - AY + Ay
#	#		AY - BX = bx - ay + aY + Ay - Bx - bX
#	#		
#	#	By re-arranging the terms, the left-hand side is now independent of the
#	#	hailstone but we still don't have a constant quantity on either side. 
#	# 	However, we know that this relationship holds for any hailstone, so we 
#	# 	can substitute a the same relationship from another hailstone in for the
#	# 	AY - BX term: 
#	#
#	#		AY - BX = eu - dv + dY + Av - Bu - eX
#	#		eu - dv + dY + Av - Bu - eX = bx - ay + aY + Ay - Bx - bX
#	#		eu - dv + dY + Av - Bu - eX - bx + ay = aY + Ay - Bx - bX
#	#		eu - dv - bx + ay = aY + Ay - Bx - bX - dY - Av + Bu + eX
#	#		eX - bX + aY - dY + Ay - Av + Bu - Bx = eu - dv - bx + ay
#	#
#	#		(e - b)X + (a - d)Y + (y - v)A + (u - x)B = eu - dv - bx + ay
#	#
#	#	Simillarly, if we swap the a/x/d/u values for c/z/f/w values:
#	#
#	#		(e - b)Z + (c - f)Y + (y - v)C + (w - z)B = ew - fv - bz + cy
#	#
#	#	For any two hailstones (x, y, z, a, b, c) and (u, v, w, d, e, f). To 
#	# 	solve for X, Y, A, B, we need a system of four linear equations. We can 
#	# 	form an equation by taking any pair of known hailstones.
#
#	hailstones = []
#	for hail_def in lines:
#		hail = tuple(int(n) for n in hail_def.replace(" @", ",").split(","))
#		hailstones.append(hail)
#	
#	eqs = 4
#	coefficients_xy = []
#	ordinates_xy = []
#	coefficients_zy = []
#	ordinates_zy = []
#
#	for hail_a, hail_b in product(hailstones, repeat=2):
#		if hail_a == hail_b:
#			continue
#		x, y, z, a, b, c = hail_a
#		u, v, w, d, e, f = hail_b
#
#		# Solves X, Y
#		coefficients_xy.append([e-b, a-d, y-v, u-x])
#		ordinates_xy.append(e*u - d*v - b*x + a*y)
#
#		# Solves Y, Z
#		coefficients_zy.append([e-b, c-f, y-v, w-z])
#		ordinates_zy.append(e*w - f*v - b*z + c*y)
#
#		eqs -= 1
#		if not eqs:
#			break
#
#	X, Y, A, B = np.linalg.solve(coefficients_xy, ordinates_xy)
#	Z, discard, C, discardagain = np.linalg.solve(coefficients_zy, ordinates_zy)
#	rock_pos = (X, Y, Z)
#	rock_vel = (A, B, C)
#	print(f"We've found X, Y, Z, and A, B, C: {rock_pos} and {rock_vel}")
#	return sum(rock_pos)

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"This is the prompt for Part One of the problem.\n")

	results = do_part_one_for(example_lines, True)
	print(f"When we do part one for the example input:")
	print(f"\tThe number of intersections in the specified region is {results}")
	print(f"\tWe expected: 2\n")

	results = do_part_one_for(input_lines, False)
	print(f"When we do part one for the actual input:")
	print(f"\tThe number of intersections in the specified region is {results}"
	   	  f"\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"What is the sum of the x, y, and z co-ordinates that you need to be"
       	  f" in such that you can throw a single rock that will destroy each ha"
		  f"il stone?\n")

	results = do_part_two_for(example_lines)
	print(f"When we do part two for the example input:")
	print(f"\tThus, the sum of X, Y, Z is {results}")
	print(f"\tWe expected: 47, after throwing the rock from (24, 13, 10) with a"
       	  f" velocity of (-3, 1, 2)\n")


	print(f"When we do part two for the actual input:")
	results = do_part_two_for(input_lines)
	print(f"\tThus, the sum of X, Y, Z is {results}\n")

def print_header():
	print("--- DAY 24: Never Tell Me The Odds ---\n")
