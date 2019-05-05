import itertools
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Infinite Sieve of Eratosthenes
# Code by David Eppstein, UC Irvine, 28 Feb 2002
# http://code.activestate.com/recipes/117119/
def gen_primes():
	""" Generate an infinite sequence of prime numbers.
	"""
	# Maps composites to primes witnessing their compositeness.
	# This is memory efficient, as the sieve is not "run forward"
	# indefinitely, but only as long as required by the current
	# number being tested.
	#
	D = {}

	# The running integer that's checked for primeness
	q = 2

	while True:
		if q not in D:
			# q is a new prime.
			# Yield it and mark its first multiple that isn't
			# already marked in previous iterations
			#
			yield q
			D[q * q] = [q]
		else:
			# q is composite. D[q] is the list of primes that
			# divide it. Since we've reached q, we no longer
			# need it in the map, but we'll mark the next
			# multiples of its witnesses to prepare for larger
			# numbers
			#
			for p in D[q]:
				D.setdefault(p + q, []).append(p)
			del D[q]

		q += 1


# Draw Ulam's spiral

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111)

cell_x = 0.5
cell_y = 0.5
num_ints = 20
primes = list(itertools.islice(gen_primes(), num_ints))

print(list(primes))

dx_sign = 1
dy_sign = 0
ints_til_turn = 1

moves = itertools.cycle([(1,0), (0, -1), (-1, 0), (0,1 )])
check = next(moves)
move, check = check, next(moves)

fin = {}

for n in range(0, num_ints):
	plt.text(cell_x, cell_y, '%s' % n, size=20)
	if n in primes:
		r = patches.Rectangle(
			(cell_x, cell_y), 0.1, 0.1,
		    linewidth=1, edgecolor='g', facecolor='b',
		)
		ax.add_patch(r)
	fin[cell_x, cell_y] = 1

	cell_x += 0.1 * move[0]
	cell_y += 0.1 * move[1]

	check_position = (
		cell_x + 0.1*check[0],
		cell_y + 0.1*check[1],
	)
	if check_position not in fin:
		move, check = check, next(moves)

plt.show()



