import itertools
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
import numpy as np
import random

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

num_ints = 350000
primes = {p: None for p in itertools.islice(gen_primes(), math.floor(num_ints/4))}

print(list(primes))
print(max(primes))

# Method from https://www.thanassis.space/primes.html
moves = itertools.cycle([(1,0), (0, -1), (-1, 0), (0,1 )])
check = next(moves)
move, check = check, next(moves)

fin = {}
size = 1

im_width, im_height = 1000, 1000
spiral = np.zeros((im_width, im_height))
cell_x = math.floor(im_width/2)
cell_y = math.floor(im_height/2)

for n in range(0, im_width*im_height):
	plt.text(cell_x, cell_y, '%s' % n, size=5, color='grey')
	if n in primes:
		if cell_x < im_width and cell_y < im_height:
			spiral[cell_x][cell_y] = 1
	fin[cell_x, cell_y] = 1

	cell_x += size * move[0]
	cell_y += size * move[1]

	check_position = (
		cell_x + size*check[0],
		cell_y + size*check[1],
	)
	if check_position not in fin:
		move, check = check, next(moves)


fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111)

print('making image')
ax.imshow(spiral, interpolation='none')
print('saving image...')
plt.savefig('D:\\media\\primes\\ulams_spiral\\batch_1_%sx%s_%s.png' % (
	im_width, im_height, random.randint(0, 10000),
))
