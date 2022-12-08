import time
import numpy as np
from numba import jit

# @jit(nopython=True) # makes generation slower but sorting faster?
def gen(length):
    return np.random.randint(0, 4294967295, length)
    # return [random.randint(0, 4294967295) for i in range(length)]

# swap as utility function
@jit(nopython=True)
def swap(array_, i1, i2):
	array_[i1], array_[i2] = array_[i2], array_[i1] 
	# temp = array_[i1]
	# array_[i1] = array_[i2]
	# array_[i2] = temp
	return array_

# partition
@jit(nopython=True)
def hoare_partition(array_, start, end):
	pivot = array_[(start + end) // 2]
	# pivot = array_[(start + end) >> 1] # equally fast
	# pivot = array_[int((start + end) / 2)] # slower

	i = start - 1
	j = end + 1

	while True:
		i += 1
		while array_[i] < pivot:
			i += 1

		j -= 1
		while array_[j] > pivot:
			j -= 1

		if i >= j:
			return j
		
		swap(array_, i, j)

# quicksort
@jit(nopython=True)
def quicksort(array_, start, end):
	if start >= 0 and end >= 0 and start < end:
		crossing = hoare_partition(array_, start, end)

		quicksort(array_, start, crossing)
		quicksort(array_, crossing + 1, end)

# length of list to generate and sort
n = 10 ** 7 # 10 Millions 

# generate and stop time
genstart = time.time_ns() # get time in nanoseconds to calculate generation time
liste = gen(n)
genend = time.time_ns()
gendiff = genend - genstart
gendiffseconds = gendiff / (10 ** 9)

# sort and stop time
sortstart = time.time_ns() # get time in nanoseconds to calculate generation time
quicksort(liste, 0, len(liste) - 1)
sortend = time.time_ns()
sortdiff = sortend - sortstart
sortdiffseconds = sortdiff / (10 ** 9)

#profile, no useful information over internals of quicksort function
# with cProfile.Profile(subcalls=True) as pr:
# 	cProfile.runctx("quicksort(liste, 0, len(liste) - 1)", None, locals())

# output results
print(f"Generation Time: {gendiff} Nanoseconds or {gendiffseconds} Seconds.")
print(f"Sorting Time: {sortdiff} Nanoseconds or {sortdiffseconds} Seconds.")