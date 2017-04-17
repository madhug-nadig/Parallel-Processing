#================================================================================================================
#----------------------------------------------------------------------------------------------------------------
#									SIMILARITY METRICS - IN PARALLEL
#----------------------------------------------------------------------------------------------------------------
#================================================================================================================

# The following code contains serial and parallelized versions of the top 5 similarity measures implemented in python. 
# The serial code is from: http://dataconomy.com/2015/04/implementing-the-five-most-popular-similarity-measures-in-python/
# Running all the algorithms one after another will have a negative imact of parallel performance due to cache related issues.

from math import pow, sqrt
from decimal import Decimal
import multiprocessing as mp
import time
from itertools import repeat


class SimilarityMetric():
	def __init__(self):
		pass

	# EUCLIDEAN DISTANCE

	#serial euclidean distance
	def serial_euclidean_distance(self,x,y):
		return sqrt(sum(pow(a-b,2) for a, b in zip(x, y)))
	
	def square(self, x, y):
		return pow(x-y,2)
	
	#parallel euclidean distance
	def parallel_euclidean_distance(self,x,y):
		pool = mp.Pool(processes= 32)
		s = time.clock()
		results = pool.starmap(self.square, zip(x,y))
		res = sqrt(sum(results))
		e = time.clock()
		print("Parallel Euclidean Exec: ", e-s)
		return res


	# MANHATTAN DISTANCE

	#serial manhattan distance
	def serial_manhattan_distance(self,x,y):
		return sum(abs(a-b) for a,b in zip(x,y))

	def sub(self, a, b):
		return abs(a-b)

	#serial manhattan distance
	def parallel_manhattan_distance(self,x,y):
		pool = mp.Pool(processes= 32)
		s = time.clock()
		results = pool.starmap(self.sub, zip(x,y))
		res = sum(results)
		e = time.clock()
		print("Parallel Manhattan Exec Time: ", e-s)
		return res

	# MINKOWSKI DISTANCE
	
	def nth_root(self, value, n_root):
		root_value = 1/float(n_root)
		return round (Decimal(value) ** Decimal(root_value),3)

	#Serial Minkowski Distance
	def serial_minkowski_distance(self, x,y,p_value):
		return self.nth_root(sum(pow(abs(a-b),p_value) for a,b in zip(x, y)),p_value)
	
	#Parallel Minkowski Distance
	
	def minkowski_helper(self,a,b,p):
			return pow(abs(a-b), p)
	
	def parallel_minkowski_distance(self, x,y,p_value):
		pool = mp.Pool(processes= 32)
		s = time.clock()
		results = pool.starmap(self.minkowski_helper, zip(x,y,repeat(p_value)))
		res = self.nth_root(sum(results), p_value)
		e = time.clock()
		print("Parallel Manhattan Exec Time: ", e-s)
		return res	
	
	
	
	#COSINE SIMILARITY
	
	#serial cosine similarity
	def square_rooted(self, x):
		return round(sqrt(sum([a*a for a in x])),3)
	
	def serial_cosine_similarity(self,x,y):
		numerator = sum(a*b for a,b in zip(x,y))
		denominator = self.square_rooted(x)*self.square_rooted(y)
		return round(numerator/float(denominator),3)
	
	def multplierr(self,a,b):
			return a*b
	
	#parallel cosine similarity
	def parallel_cosine_similarity(self,x,y):

		pool = mp.Pool(processes= 16)
		s = time.clock()
		nums = pool.starmap(self.multplierr, zip(x,y))
		numerator = sum(nums)
		
		#x_sqr = pool.starmap( self.multplierr, zip(x,x))
		#y_sqr = pool.starmap( self.multplierr, zip(y,y))
		
		#denominator = round(sqrt(sum(x_sqr))) * round(sqrt(sum(y_sqr)))
		denominator = self.square_rooted(x)*self.square_rooted(y)
		
		e = time.clock()
		print("Parallel Cosine Exec Time: ", e-s)
		return round(numerator/float(denominator),3)

	#JACCARD SIMILARITY
	
	#Serial Jaccard Similarity
	def serial_jaccard_similarity(self, x,y):
		intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
		union_cardinality = len(set.union(*[set(x), set(y)]))
		print(intersection_cardinality, union_cardinality)
		return intersection_cardinality/float(union_cardinality)
	


	def interc_card_locl(self, x,y):
		return len(set.intersection(*[set(x), set(y)]))
	
	def union_card_locl(self,x,y):
		return len(set.union(*[set(x), set(y)]))
		
	#Parallel Jaccard Similarity
	def parallel_jaccard_similarity(self,x,y):

		p = 16
		pool = mp.Pool(processes= p)

		chunk_X = []
		chunk_Y = []

		for i in range(0, len(x), p):

			chunk_X.append(x[int(i):int((i+1)*p)])
			chunk_Y.append(y[int(i):int((i+1)*p)])

		s = time.clock()

		intersection_cardinality = sum(pool.starmap(self.interc_card_locl, zip(chunk_X,chunk_Y)))
		union_cardinality = sum(pool.starmap(self.union_card_locl, zip(chunk_X,chunk_Y)))
		print(intersection_cardinality, union_cardinality)
		e = time.clock()
		print("Parallel Jaccard Exec Time: ", e-s)
		return intersection_cardinality/float(union_cardinality)

def main():
	sm = SimilarityMetric()
	
	# Jaccard Similarity
	s = time.clock()
	print("Jaccard Similarity: ", sm.serial_jaccard_similarity([x for x in range(0,30000,3)], [x for x in range(0,20000,2)]))
	e = time.clock()
	print("Serial Jaccard  Time: ", e-s)
	print("Parallel Jaccard similarity: ", sm.parallel_jaccard_similarity([x for x in range(0,30000,3)], [x for x in range(0,20000,2)]))
	
	# Cosine Similarity
	s = time.clock()
	print("Cosine similarity: ", sm.serial_cosine_similarity([x for x in range(0,30000000,3)], [x for x in range(0,20000000,2)]))
	e = time.clock()
	print("Serial Cosine  Time: ", e-s)
	print("Parallel Cosine similarity: ", sm.parallel_cosine_similarity([x for x in range(0,30000000,3)], [x for x in range(0,20000000,2)]))

	# Minkowski Distance
	s = time.clock()
	print("Minkowski Distance: ", sm.serial_minkowski_distance([x for x in range(0,30000000,3)], [x for x in range(0,20000000,2)],3))
	e = time.clock()
	print("Serial Minkowski Distance  Time: ", e-s)
	print("Parallel Minkowski Distance similarity: ", sm.parallel_minkowski_distance([x for x in range(0,30000000,3)], [x for x in range(0,20000000,2)], 3))

	# Manhattan Distance
	s = time.clock()
	print("Manhattan Distance: ", sm.serial_manhattan_distance([x for x in range(0,30000000,3)], [x for x in range(0,20000000,2)]))
	e = time.clock()
	print("Serial Manhattan  Time: ", e-s)
	print("Parallel Manhattan Distance: ", sm.parallel_manhattan_distance([x for x in range(0,30000000,3)], [x for x in range(0,20000000,2)]))
	
	# Euclidean Distance
	s = time.clock()
	print("Euclidean Distance: ", sm.serial_euclidean_distance([x for x in range(0,30000000,3)], [x for x in range(0,20000000,2)]))
	e = time.clock()
	print("Serial Euclidean  Time: ", e-s)
	print("Parallel Euclidean Distance: ", sm.parallel_euclidean_distance([x for x in range(0,30000000,3)], [x for x in range(0,20000000,2)]))


if __name__ == '__main__':
	main()

