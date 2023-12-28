# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

from itertools import product
import numpy as np

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

def do_part_two_for(lines):
	# So, I *did* code this independently and did the math by myself, but it was
	# following someone else's solution/instructions and checking my math 
	# against theirs. It's been a long time since my linear algebra course...
	#
	#	Let Rock Position = X, Y, Z		Let Hailstone i Position = x, y, z
	#	Let Rock Velocity = A, B, C		Let Hailstone i Velocity = a, b, c
	#	
	#	At some time t, the new Rock Position is:
	#
	#		X + tA, Y + tB, Z + tC
	#
	#	And it intersects with some hailstone: 
	#
	#		x + ta, y + tb, z + tc
	#
	#	Using the x positions we can find an equation for t:
	#
	#		X + tA = x + ta
	#		X + tA - x = ta
	#		X - x = ta - tA
	#		X - x = t(a - A)
	#		t = (X - x)/(a - A)
	#
	#	And the same holds for y, z:
	#
	#		t = (Y - y)/(b - B), (Z - z)/(c - C)
	#
	#	So we know t in terms of x, y, so we can express an equality entirely in
	# 	terms of x, y:
	#
	#		(X - x)/(a - A) = (Y - y)/(b - B)
	#		(b - B)(X - x) = (a - A)(Y - y)
	#		bX - bx - BX + Bx = aY - ay - AY + Ay
	#		AY - BX = bx - ay + aY + Ay - Bx - bX
	#		
	#	By re-arranging the terms, the left-hand side is now independent of the
	#	hailstone but we still don't have a constant quantity on either side. 
	# 	However, we know that this relationship holds for any hailstone, so we 
	# 	can substitute a the same relationship from another hailstone in for the
	# 	AY - BX term: 
	#
	#		AY - BX = eu - dv + dY + Av - Bu - eX
	#		eu - dv + dY + Av - Bu - eX = bx - ay + aY + Ay - Bx - bX
	#		eu - dv + dY + Av - Bu - eX - bx + ay = aY + Ay - Bx - bX
	#		eu - dv - bx + ay = aY + Ay - Bx - bX - dY - Av + Bu + eX
	#		eX - bX + aY - dY + Ay - Av + Bu - Bx = eu - dv - bx + ay
	#
	#		(e - b)X + (a - d)Y + (y - v)A + (u - x)B = eu - dv - bx + ay
	#
	#	Simillarly, if we swap the a/x/d/u values for c/z/f/w values:
	#
	#		(e - b)Z + (c - f)Y + (y - v)C + (w - z)B = ew - fv - bz + cy
	#
	#	For any two hailstones (x, y, z, a, b, c) and (u, v, w, d, e, f). To 
	# 	solve for X, Y, A, B, we need a system of four linear equations. We can 
	# 	form an equation by taking any pair of known hailstones.

	hailstones = []
	for hail_def in lines:
		hail = tuple(int(n) for n in hail_def.replace(" @", ",").split(","))
		hailstones.append(hail)
	
	eqs = 4
	coefficients_xy = []
	ordinates_xy = []
	coefficients_zy = []
	ordinates_zy = []

	for hail_a, hail_b in product(hailstones, repeat=2):
		if hail_a == hail_b:
			continue
		x, y, z, a, b, c = hail_a
		u, v, w, d, e, f = hail_b

		# Solves X, Y
		coefficients_xy.append([e-b, a-d, y-v, u-x])
		ordinates_xy.append(e*u - d*v - b*x + a*y)

		# Solves Y, Z
		coefficients_zy.append([e-b, c-f, y-v, w-z])
		ordinates_zy.append(e*w - f*v - b*z + c*y)

		eqs -= 1
		if not eqs:
			break

	X, Y, A, B = np.linalg.solve(coefficients_xy, ordinates_xy)
	Z, discard, C, discardagain = np.linalg.solve(coefficients_zy, ordinates_zy)
	rock_pos = tuple([round(v) for v in (X, Y, Z)])
	rock_vel = tuple([round(v) for v in (A, B, C)])
	print(f"We've found X, Y, Z, and A, B, C: {rock_pos} and {rock_vel}")
	return sum(rock_pos)

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
