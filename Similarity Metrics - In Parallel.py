#================================================================================================================
#----------------------------------------------------------------------------------------------------------------
#									SIMILARITY METRICS - IN PARALLEL
#----------------------------------------------------------------------------------------------------------------
#================================================================================================================

# The following code contains serial and parallelized versions of the top 5 similarity measures implemented in python. 
# The serial code is from: http://dataconomy.com/2015/04/implementing-the-five-most-popular-similarity-measures-in-python/

from math import pow, sqrt
from decimal import Decimal
import multiprocessing as mp
import time

class SimilarityMetric():
	def __init__(self):
		pass

	def serial_euclidean_distance(self,x,y):
		return sqrt(sum(pow(a-b,2) for a, b in zip(x, y)))
	
	def square(self, x, y):
		return pow(x-y,2)
	
	def parallel_euclidean_distance(self,x,y):
		pool = mp.Pool(processes= 32)
		s = time.clock()
		results = pool.starmap(self.square, zip(x,y))
		res = sqrt(sum(results))
		e = time.clock()
		print("Parallel Euclidean Exec: ", e-s)
		return res
	
	def serial_manhattan_distance(self,x,y):
		return sum(abs(a-b) for a,b in zip(x,y))

	def sub(self, a, b):
		return abs(a-b)
	
	def parallel_manhattan_distance(self,x,y):
		pool = mp.Pool(processes= 32)
		s = time.clock()
		results = pool.starmap(self.sub, zip(x,y))
		res = sum(results)
		e = time.clock()
		print("Parallel Manhattan Exec Time: ", e-s)
		return res

	def nth_root(self, value, n_root):
		root_value = 1/float(n_root)
		return round (Decimal(value) ** Decimal(root_value),3)

	def serial_minkowski_distance(self, x,y,p_value):
		return self.nth_root(sum(pow(abs(a-b),p_value) for a,b in zip(x, y)),p_value)

	def square_rooted(self, x):
		return round(sqrt(sum([a*a for a in x])),3)

	def serial_cosine_similarity(self,x,y):
		numerator = sum(a*b for a,b in zip(x,y))
		denominator = self.square_rooted(x)*self.square_rooted(y)
		return round(numerator/float(denominator),3)

	def serial_jaccard_similarity(self, x,y):
		intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
		union_cardinality = len(set.union(*[set(x), set(y)]))
		return intersection_cardinality/float(union_cardinality)

def main():
	sm = SimilarityMetric()

	# print("Jaccard Similarity: ", sm.serial_jaccard_similarity([3, 45, 7, 2], [2, 54, 13, 15]))
	# print("Cosine similarity: ", sm.serial_cosine_similarity([3, 45, 7, 2], [2, 54, 13, 15]))
	# print("Minkowski Distance: ", sm.serial_minkowski_distance([3, 45, 7, 2], [2, 54, 13, 15],3))
	
	s = time.clock()
	print("Manhattan Distance: ", sm.serial_manhattan_distance([x for x in range(0,30000000,3)], [x for x in range(0,20000000,2)]))
	e = time.clock()
	print("Serial Manhattan  Time: ", e-s)
	print("Parallel Manhattan Distance: ", sm.parallel_manhattan_distance([x for x in range(0,30000000,3)], [x for x in range(0,20000000,2)]))
	
	
	s = time.clock()
	print("Euclidean Distance: ", sm.serial_euclidean_distance([x for x in range(0,30000000,3)], [x for x in range(0,20000000,2)]))
	e = time.clock()
	print("Serial Euclidean  Time: ", e-s)
	print("Parallel Euclidean Distance: ", sm.parallel_euclidean_distance([x for x in range(0,30000000,3)], [x for x in range(0,20000000,2)]))


if __name__ == '__main__':
	main()

