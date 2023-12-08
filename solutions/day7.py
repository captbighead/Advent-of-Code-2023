# Imports from personal library
from utilities.vector import vector
import utilities.algos as algos
import utilities.io as io

# Imports from standard libraries I find myself using all the time
from collections import defaultdict
from collections import deque

try:
	input_lines = io.read_input_as_lines(7)
	example_lines = io.read_example_as_lines(7)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Example"]

CARD_RANK = {c: 13-i for i, c in enumerate("AKQJT98765432")}
CARD_RANK_P2 = {c: 13-i for i, c in enumerate("AKQT98765432J")}

class camel_cards_hand:

	def __init__(self, hand, bid) -> None:
		self.bid = bid
		self.hand_literal = hand
		self.hand_numeric = [self.hand_class()]
		self.hand_numeric.extend([CARD_RANK[c] for c in hand])
		self.hand_numeric = tuple(self.hand_numeric)

	def hand_class(self):
		hstr = self.hand_literal
		counts = {c: hstr.count(c) for c in hstr}
		diff_cards = len(counts.keys())

		if diff_cards == 1:
			return 107
		elif diff_cards == 2 and 4 in counts.values():
			return 106
		elif diff_cards == 2 and 3 in counts.values() and 2 in counts.values():
			return 105
		elif diff_cards == 3 and 3 in counts.values():
			return 104
		elif diff_cards == 3 and 2 in counts.values():
			return 103
		elif diff_cards == 4:
			return 102
		else:
			return 101
		
	def __repr__(self) -> str:
		return f"{self.hand_literal} {self.bid}"
	
class camel_cards_hand_p2:

	def __init__(self, hand, bid) -> None:
		self.bid = bid
		self.hand_literal = hand
		self.hand_numeric = [self.hand_class()]
		self.hand_numeric.extend([CARD_RANK_P2[c] for c in hand])
		self.hand_numeric = tuple(self.hand_numeric)

	def hand_class(self):
		hstr = self.hand_literal
		counts = {c: hstr.count(c) for c in hstr}

		# Here, if there is a J, we convert it into the version of itself that 
		# would give the best hand:
		if counts.get("J", False):
			alias = self.alias_hand()
			counts = {c: alias.count(c) for c in alias}

		diff_cards = len(counts.keys())

		if diff_cards == 1:
			return 107
		elif diff_cards == 2 and 4 in counts.values():
			return 106
		elif diff_cards == 2 and 3 in counts.values() and 2 in counts.values():
			return 105
		elif diff_cards == 3 and 3 in counts.values():
			return 104
		elif diff_cards == 3 and 2 in counts.values():
			return 103
		elif diff_cards == 4:
			return 102
		else:
			return 101

	def alias_hand(self):
		hstr = self.hand_literal
		jokers = hstr.count("J")	# Find out how many wild cards there are

		# Remove them. We can operate off of the new set. 
		hstr = hstr.replace("J", "")
		counts = {c: hstr.count(c) for c in hstr}
		cards_we_have = sorted(list(counts.keys()), key=lambda c: counts[c], reverse=True)
		diff_cards = len(cards_we_have)

		# This is actually so simple but I had to prove it out by iterating 
		# possibilities in my head: the rule is just make all jokers you have 
		# into any card you have the most of.
		#
		# If we have 4 or 3 of something, and we know we have at least 1 joker,
		# converting all the jokers we have gives us a 5 or 4 of a kind.
		# 
		# If we have 2 of something, We know the most we have of any one card is
		# 2, so we have 1-3 jokers. 
		#
		# 	- 3 Jokers: Make them match the pair, we have 5 of a kind
		# 	- 2 Jokers: Make them match the pair, we have 4 of a kind
		# 	- 1 Jokers: We either have 2 pair, so we end up with a full house,
		# 			or we have  2, 1, 1 of something, so making it match the 
		# 			pair gives us a 3 of a kind 
		#
		# That leaves us with the case where we only have 1 of each of the cards
		# we have. We have 1 - 4 jokers:
		# 
		# 	- 4 Jokers: Make it match, we have 5 of a kind
		# 	- 3 Jokers: Make it match one of them, we have 4 of a kind. 
		# 	- 2 Jokers: Making them both match still gets us 3 of a kind, which
		# 			beats our other option of 2 pair. 
		# 	- 1 Joker: Any pair will do!
		return hstr + ((cards_we_have[0] if cards_we_have else "J") * jokers) 

	def __repr__(self) -> str:
		return f"{self.hand_literal} ({self.alias_hand()}) {self.bid}"

def do_part_one_for(lines):
	L = len(lines) + 1
	cc_hands = []
	for line in lines:
		h, b = line.split()
		cc_hands.append(camel_cards_hand(h, int(b)))
	cc_hands = sorted(cc_hands, reverse=True, key=lambda cch: cch.hand_numeric)
	rnkd = [((L-i), (L-i) * cch.bid, cch) for i, cch in enumerate(cc_hands, 1)]
	return sum((L-i) * cch.bid for i, cch in enumerate(cc_hands, 1))


def do_part_two_for(lines):
	L = len(lines) + 1
	cc_hands = []
	for line in lines:
		h, b = line.split()
		cc_hands.append(camel_cards_hand_p2(h, int(b)))
	cc_hands = sorted(cc_hands, reverse=True, key=lambda cch: cch.hand_numeric)
	rnkd = [((L-i), (L-i) * cch.bid, cch) for i, cch in enumerate(cc_hands, 1)]
	return sum((L-i) * cch.bid for i, cch in enumerate(cc_hands, 1))

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"This is the prompt for Part One of the problem.\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe total winnings of all of the hands is {results}")
	print(f"\tWe expected: 6440\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe total winnings of all of the hands is {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"This is the prompt for Part Two of the problem.\n")

	results = do_part_two_for(example_lines)
	print(f"When we do part two for the example input:")
	print(f"\tThe winnings when jokers are wild is {results}")
	print(f"\tWe expected: 5905\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe winnings when jokers are wild is {results}\n")	# NOT 248459417

def print_header():
	print("--- DAY 7: Camel Cards ---\n")
