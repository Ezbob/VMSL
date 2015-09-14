from math import sqrt
from math import fsum
from numbers import Real
from copy import copy
from random import random

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
			temp = []
			for i in range(n):
				temp.append(0.)
			return cls(temp)
		else:
			raise ValueError("Dimension of zero vector must be a postive non-zero value")

	@classmethod
	def random(cls,n = 1, mod = 100):
		if n > 0:
			temp = []
			for i in range(n):
				temp.append( (random() * mod) - mod/2 )
			return cls(temp)
		else:
			raise ValueError("Dimension of zero vector must be a postive non-zero value")

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

	# alternative to the dimension method
	def __len__(self):
		return self.dimension()

	# supports iteration
	def __iter__(self):
		return self.coordinates.__iter__()

	# string representation of a instance of the vector class
	def __repr__(self):
		return "("+ str(self.coordinates).strip("[]") + ")^T"

	# enables coordination retrival
	def __getitem__(self,index):
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
				tempCoords = []
				for x in range(len(self.coordinates)):
					tempCoords.append(self.coordinates[x] + other.coordinates[x])
				return vector(tempCoords)
			else:
				raise ValueError("Vector dimensions does not match") 
		elif isinstance(other, int) or isinstance(other,float): # scalar addision
			tempCoords = []
			for x in range(len(self.coordinates)):
				tempCoords.append(self.coordinates[x] + other)
			return vector(tempCoords)
		else:
			raise TypeError("Undefined vector operation with " + str(other.__class__))
	
	# allowing for commutative addition
	def __radd__(self,inp):
		return self.__add__(inp)

	def __sub__(self,other): # vector and scalar subtraction
		if isinstance(other, vector):
			if len(other.coordinates) == len(self.coordinates):
				tempCoords = []
				for x in range(len(self.coordinates)):
					tempCoords.append(self.coordinates[x] - other.coordinates[x])
				return vector(tempCoords)
			else:
				raise ValueError("Vector dimensions does not match")
		elif isinstance(other, int) or isinstance(other,float):
			tempCoords = []
			for x in range(len(self.coordinates)):
				tempCoords.append(self.coordinates[x] - other)
			return vector(tempCoords)
		else:
			raise TypeError("Undefined vector operation with " + str(other.__class__))

	# vector and scalar multiplication
	def __mul__(self,other):
		if isinstance(other, int) or isinstance(other, float): # scalar multi
			tempCoords = []
			for x in range(len(self.coordinates)):
				tempCoords.append(self.coordinates[x]*other) 
			return vector(tempCoords)
		elif isinstance(other, vector): # dot product
			if len(other.coordinates) == len(self.coordinates):
				return fsum((self.coordinates[i]*other.coordinates[i]) for i in range(len(self.coordinates)))
			else:
				raise ValueError("Vector dimensions does not match")
		else:
			raise TypeError("Undefined vector operation with " + str(other.__class__))
	
	# allowing for scalar commutative multiplication
	def __rmul__(self,inp): 
		return self.__mul__(inp);

	# scalar division
	def __div__(self,other): 
		if (isinstance(other,int) or isinstance(other,float)) and other != 0: # scalar div
			tempCoords = []
			for x in range(len(self.coordinates)):
				tempCoords.append(self.coordinates[x]/other) 
			return vector(tempCoords)
		elif other == 0:
			raise ZeroDivisionError("division with zero error")
		else:
			raise TypeError("Undefined vector operation with " + str(other.__class__))
	
	# dimension of the vector
	def dimension(self): 
		return len(self.coordinates)

	def transpose(self):
		result = []
		for i in range():
			result.append(self[i])
		return result

	# length(norm) of the vector
	def length(self):
		temp = 0
		for x in range(self.dimension()):
			temp += self.coordinates[x]**2
		return sqrt(temp)

	# an alias function for length()
	def norm(self):
		return self.length()
	# get the coordiantes
	def getCoordinates(self):
		return self.coordinates
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
			result = []
			for i in range(n):
				temp = []
				for j in range(n):
					if i == j:
						temp.append(1)
					else:
						temp.append(0)
					if j == n-1:
						result.append(vector(temp))
			return cls(result)
		else:
			raise ValueError("Dimension of identity matrix must be a positve non-zero value")	

	@classmethod
	def random(cls,n = 1, m = 0, mod = 100):
		if (n > 0):
			result = []
			if m > 0:
				for i in range(m):
					result.append(vector.random(n,mod))	
			else:
				for i in range(n):
					result.append(vector.random(n,mod))
			return cls(result)
		else:
			raise ValueError("Dimension of identity matrix must be a positve non-zero value") 

	@classmethod
	def zeros(cls,n = 1, m = 0):
		if (n > 0):
			result = []
			if m > 0:
				for i in range(m):
					result.append(vector.zeros(n))
			else:
				for i in range(n):
					result.append(vector.zeros(n))
			return cls(result)
		else:
			raise ValueError("Dimension of identity matrix must be a positve non-zero value")

	def __init__(self, *vectors):
		if isinstance(vectors[0],list):
			self.columnVectors = vectors[0]
		else:
			self.columnVectors = list(vectors) # only vectors allowed
		if all(isinstance(elm,vector) for elm in self.columnVectors) == False:
			raise TypeError("Mixed types in matrix initialization")
	
	# string representation for instance of the class
	def __repr__(self):
		results = str()
		for i in range(self.dimensions()[0]):
			results += "["
			for j in range(self.dimensions()[1]):	
				results += " %12.6f " % self[j][i]
				if (j == self.dimensions()[1]-1):
					results += "] \n"
		return results 

	# acts like a double dimensional list; supporting row and column indexing
	def __getitem__(self,index):
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

	# trucate the matrix to the desired size by deleting components
	def truncate(self,m = -1,n = -1):
		if m > 0 or n > 0:
			result = []
			for i in range(m):
				result.append(self.columnVectors[i].truncate(n))
			return matrix(result)
		else:
			raise ValueError("Argument error: Cannot resize matrix")
