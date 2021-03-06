from math import sqrt
from math import fsum
from numbers import Real
from copy import copy
from random import random
from itertools import izip

VM_DEFAULT_SHOW_DIST = 50

## By Anders Busch (2014)
__author__ = "Anders Busch"
## --Vectors-- ##

class vector(object):
	"""
	This is a vector class for vectors in the real number domain.
	"""
	# returns a zero vector with specified dimension
	@classmethod
	def zeros(cls,n = 1):
		if n > 0:
			return cls([0 for x in xrange(n)])
		else:
			raise ValueError("Dimension of zero vector must be a postive non-zero value")

	@classmethod
	def random(cls,n = 1, mod = 100):
		if n > 0:
			return cls([(random() * mod) - mod/2 for x in xrange(n)])
		else:
			raise ValueError("Dimension of zero vector must be a postive non-zero value")
	def __len__(self):
		return self.dimension()
	
	def __init__(self,*cords):
		if cords == None:
			self.coordinates = []
		elif isinstance(cords[0],list):
			self.coordinates = cords[0]
		else:
			self.coordinates = list(cords)
		# only real type supported
		if all(isinstance(elm,Real) for elm in self.coordinates) == False:
			raise TypeError("Mixed types in vector initialization")
		self.showDist = VM_DEFAULT_SHOW_DIST

	# alternative to the dimension method
	def __len__(self):
		return self.dimension()

	# supports iteration
	def __iter__(self):
		return self.coordinates.__iter__()

	# string representation of a instance of the vector class
	def __repr__(self):
		if self.showDist >= len(self.coordinates):  
			return "("+ str(self.coordinates).strip("[]") + ")^T"
		elif self.showDist < 0:
			raise ValueError("Got negative show distance")
		else:
			return "vector: members > %i " % self.showDist

	# enables coordination retrival
	def __getitem__(self,index):
		if isinstance(index,slice):
			return vector(self.coordinates[index])	
		else:
			return self.coordinates[index]

	# enables coordination manipulation
	def __setitem__(self,index,other):
		if isinstance(other,Real):
			self.coordinates[index] = other
		else:
			raise TypeError("Attempt to mix type in vector declaration")

	# equality checking
	def __eq__(self,other):
		if isinstance(other,vector):
			return self.coordinates == other.coordinates
		else:
			return self.coordinates == other

	# inequality (negation) checking
	def __ne__(self,other):
		if isinstance(other,vector):
			return not (self.__eq__(other))
		else:
			raise TypeError("Undefined vector relation with " + str(other.__class__))

	# scalar and vector addition
	def __add__(self,other):
		if isinstance(other, vector): # vector addition
			if len(other.coordinates) == len(self.coordinates):
				return vector([ x + y for x , y in izip(self.coordinates, other.coordinates) ])
			else:
				raise ValueError("Vector dimensions does not match") 
		elif isinstance(other, int) or isinstance(other,float): # scalar addision
			return vector([ x + other for x in self.coordinates ])
		else:
			raise TypeError("Undefined vector operation with " + str(other.__class__))
	
	# allowing for commutative addition
	def __radd__(self, other):
		return self.__add__(other)

	def __sub__(self, other): # vector and scalar subtraction
		if isinstance(other, vector):
			if len(other.coordinates) == len(self.coordinates):
				return vector([ x - y for x , y in izip(self.coordinates, other.coordinates) ])
			else:
				raise ValueError("Vector dimensions does not match")
		elif isinstance(other, int) or isinstance(other,float):
			return vector([ x - other for x in self.coordinates ])
		else:
			raise TypeError("Undefined vector operation with " + str(other.__class__))

	# vector and scalar multiplication
	def __mul__(self, other):
		if isinstance(other, int) or isinstance(other, float): # scalar multi
			return vector([ x * other for x in self.coordinates ])
		elif isinstance(other, vector): # dot product
			if len(other.coordinates) == len(self.coordinates):
				return fsum((x * y) for x,y in izip(self.coordinates, other.coordinates))
			else:
				raise ValueError("Vector dimensions does not match")
		else:
			raise TypeError("Undefined vector operation with " + str(other.__class__))
	
	# allowing for scalar commutative multiplication
	def __rmul__(self, other): 
		return self.__mul__(other);

	# scalar division
	def __div__(self, other): 
		if (isinstance(other, int) or isinstance(other, float)) and other != 0: # scalar div
			return vector([x / other for x in self.coordinates])
		elif other == 0:
			raise ZeroDivisionError("division with zero error")
		else:
			raise TypeError("Undefined vector operation with " + str(other.__class__))
	
	# dimension of the vector
	def dimension(self): 
		return len(self.coordinates)

	# length(norm) of the vector
	def length(self):
		return sqrt(sum([x ** 2 for x in self.coordinates ]))

	# an alias function for length()
	def norm(self):
		return self.length()

	# get the coordiantes
	def getCoordinates(self):
		return self.coordinates

	def getShowDistance(self):
		return self.showDist

	# truncate the vector deleting components
	def truncate(self,n):
		if n > 0 and n < len(self.coordinates)+1:
			return vector(self.coordinates[:n]) 
		else:
			raise ValueError("Error: Cannot truncate vector, invalid Argument")


## -- matrices -- ##

class matrix(object):
	"""
	Matrix combining the vector class to form a matrix
	"""
	# class method for constructing a indentity matrix
	@classmethod
	def identity(cls,n = 1):
		if (n > 0):
			return cls([ vector([ int(x == y) for y in xrange(n) ]) for x in xrange(n)])
		else:
			raise ValueError("Dimension of identity matrix must be a positve non-zero value")	

	@classmethod
	def random(cls,n = 1, m = 0, mod = 100):
		if (n > 0):
			if m > 0:
				return cls([ vector.random(n, mod) for v in xrange(m) ])
			else:
				return cls([ vector.random(n, mod) for v in xrange(n) ])
		else:
			raise ValueError("Dimension of identity matrix must be a positve non-zero value") 

	@classmethod
	def zeroes(cls,n = 1, m = 0):
		if (n > 0):
			if m > 0:
				return cls([ vector.zeros(n) for v in xrange(m) ])
			else:
				return cls([ vector.zeros(n) for v in xrange(n) ])
		else:
			raise ValueError("Dimension of identity matrix must be a positve non-zero value")

	def __init__(self, *vectors):
		if isinstance(vectors[0],list):
			self.columnVectors = vectors[0]
		else:
			self.columnVectors = list(vectors) # only vectors allowed
		if not all( isinstance(elem, vector) for elem in self.columnVectors ):
			raise TypeError("Mixed types in matrix initialization")
		self.showDist = VM_DEFAULT_SHOW_DIST
	
	# string representation for instance of the class
	def __repr__(self):
		if sum(self.dimensions()) > self.showDist:
			return "matrix: members > %i" % self.showDist
		elif self.showDist < 0:
			raise ValueError("Got negative show distance")
		results = ""
		for i in range(self.dimensions()[0]):
			results += "["
			for j in range(self.dimensions()[1]):	
				results += " %12.6f " % self[j][i]
				if (j == self.dimensions()[1]-1):
					results += "] \n"
		return results 

	# acts like a double dimensional list; supporting row and column indexing
	def __getitem__(self,index):
		if isinstance(index, tuple) and len(index) == 2:
			if all( isinstance(e, slice) for e in index ):
				return matrix([ v[index[0]] for v in self.columnVectors[index[1]]])
			if all( isinstance(e, int) for e in index):
				return self.columnVectors[index[1]][index[0]]
		else:
			return self.columnVectors[index]

	# set column vectors in matrix
	def __setitem__(self,index,other):
		if isinstance(other,vector):
			self.columnVectors[index] = other
		else:
			raise TypeError("Attempt to mix type in matrix declaration")

	
	# check equality between matrices and other types
	def __eq__(self,other):
		if isinstance(other,matrix):
			return self.columnVectors == other.columnVectors
		else:
			return self.columnVectors == other
	
	# check for negative equality between matrices and other types
	def __ne__(self,other):
		return not (self.__eq__(other))
	
	# matrix addition
	def __add__(self, other):
		if isinstance(other, matrix): # matrix
			if self.dimensions() == other.dimensions():
				results = []
				for i in range(len(self.columnVectors)):
					results.append(self[i] + other[i])
				return matrix(results)
			else:
				raise ValueError("Matrix dimensions does not match") 
		else:
			raise TypeError("Undefined matrix operation with " + str(other.__class__))

	# matrix subtraction
	def __sub__(self, other):
		if isinstance(other, matrix):
			if self.dimensions() == other.dimensions():
				results = []
				for i in range(len(self.columnVectors)):
					results.append(self.columnVectors[i] - other.columnVectors[i])
				return matrix(results)
			else:
				raise ValueError("Matrix dimensions does not match") 
		else:
			raise TypeError("Undefined matrix operation with " + str(other.__class__))
	
	# scalar multiplication and simple matrix multiplication
	def __mul__(self, other):
		if isinstance(other, int) or isinstance(other, float): # scalar
			results = []
			for i in range(len(self.columnVectors)):
				results.append(self[i] * other)
			return matrix(results)
		elif isinstance(other, matrix): # matrix
			if self.dimensions()[1] == other.dimensions()[0]:
				results = []
				m = self.dimensions()[1]
				n = other.dimensions()[1]
				for i in range(m):
					tempList = []
					for j in range(n):
						tempList.append(self.getRowVector(i)*other[j])
						if j == n-1:
							results.append(vector(tempList))
				return matrix(results).transpose()
			else:
				raise ValueError("Row and columns dimensions does not match") 
		elif isinstance(other,vector):
			if self.dimensions()[1] == self.dimensions()[0]:
				if len(other.coordinates) == self.dimensions()[1]:
					trans = self.transpose()
					dim = self.dimensions()[0]
					results = []
					for i in range(dim):
						results.append(trans[i] * other)
					return vector(results)
				else:
					raise ValueError("vector and matrix dimensions does not match")	
			else:
				raise ValueError("Not a square matrix")
		else:
			raise TypeError("Undefined matrix operation with " + str(other.__class__))

	# scalar multiplication is commutative
	def __rmul__(self,other):
		return self.__mul__(other);

	# scalar divition
	def __div__(self, other):
		if isinstance(other,int) or isinstance(other,float) and other != 0: # scalar
			results = []
			for i in range(len(self.columnVectors)):
				results.append(self[i] / other)
			return matrix(results)
		elif other == 0:
			raise ZeroDivisionError("division with zero error")
		else:
			raise TypeError("Undefined matrix operation with " + str(other.__class__))

	# get matrix dimensions as (row,column) tuple
	def dimensions(self):
		return (len(self[0].coordinates),len(self.columnVectors))

	# returns the transpose of this matrix
	def transpose(self):
		results = []
		for i in range(self.dimensions()[0]):
			tempList = []
			results.append(self.getRowVector(i))
		return matrix(results)

	# returns rows as row vectors
	def getRowVector(self,index):
		result = []
		for i in range(self.dimensions()[1]):
			result.append(self[i][index])
		return vector(result)

	def getShowDistance(self):
		return self.showDist

	# trucate the matrix to the desired size by deleting components
	def truncate(self,m = -1,n = -1):
		if m > 0 or n > 0:
			result = []
			for i in range(m):
				result.append(self.columnVectors[i].truncate(n))
			return matrix(result)
		else:
			raise ValueError("Argument error: Cannot resize matrix")
