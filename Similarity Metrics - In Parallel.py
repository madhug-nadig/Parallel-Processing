#================================================================================================================
#----------------------------------------------------------------------------------------------------------------
#									SIMILARITY METRICS - IN PARALLEL
#----------------------------------------------------------------------------------------------------------------
#================================================================================================================

# The following code contains serial and parallelized versions of the top 5 similarity measures implemented in python. 
# The serial code is from: http://dataconomy.com/2015/04/implementing-the-five-most-popular-similarity-measures-in-python/

from math import pow, sqrt
from decimal import Decimal


class SimilarityMetric():
	def __init__(self):
		pass

	def serial_euclidean_distance(self,x,y):
		return sqrt(sum(pow(a-b,2) for a, b in zip(x, y)))

	def serial_manhattan_distance(self,x,y):
		return sum(abs(a-b) for a,b in zip(x,y))

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
		
	

sm = SimilarityMetric()

print("Jaccard Similarity: ", sm.serial_jaccard_similarity([3, 45, 7, 2], [2, 54, 13, 15]))
print("Cosine similarity: ", sm.serial_cosine_similarity([3, 45, 7, 2], [2, 54, 13, 15]))
print("Minkowski Distance: ", sm.serial_minkowski_distance([3, 45, 7, 2], [2, 54, 13, 15],3))
print("Manhattan Distance: ", sm.serial_manhattan_distance([3, 45, 7, 2], [2, 54, 13, 15]))
print("Euclidean Distance: ", sm.serial_euclidean_distance([3, 45, 7, 2], [2, 54, 13, 15]))