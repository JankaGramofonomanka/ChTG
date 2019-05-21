from math import sqrt

from misc import iterable

class Circle():

	def __init__(self, center, radius):
		
		if not iterable(center) or len(center) != 2:
			raise TypeError("Argument 'center' must be iterable, of legth 2")

		self.center = center

		try:
			self.radius = float(radius)
			if self.radius < 0:
				raise TypeError("Argument 'radius' must be greater or equal to 0")

		except TypeError:
			raise TypeError("Argument 'radius' must be a number")

	def __contains__(self, point):
		return dist(point, self.center) < self.radius

class ClosedCircle(Circle):

	def __init__(self, center, radius):
		Circle.__init__(self, center, radius)

	def __contains__(self, point):
		return dist(point, self.center) <= self.radius


class Vector():
	
	def __init__(self, coords):
		
		if iterable(coords, TypeError('coords must be iterable')):
			self.coords= tuple(coords)

	def __add__(self, w):
		if iterable(w) and len(w) == len(self):
	
			coords = []
			for i in range(len(self)):
				coords.append(self[i] + w[i])

			return Vector(coords)

	def __iadd__(self, w):
		if iterable(w) and len(w) == len(self):
			return self + w
		else:
			raise ValueError

	def __neg__(self):
		coords = []
		for i in range(len(self)):
			coords.append(-self[i])

		return Vector(coords)

	def __sub__(self, w):
		if iterable(w) and len(self) == len(w):
			return self + (-w)
		else:
			raise ValueError		

	def __mul__(self, w):
		"""This is a dot product"""

		if iterable(w) and len(self) == len(w):
			result = 0
			for i in range(len(self)):
				result += self[i]*w[i]

			return result
		else:
			return Vector([c*coord for coord in self.coords])

	def __rmul__(self, c):
		if iterable(c):
			return self*c
		else:
			return Vector([c*coord for coord in self.coords])

	def __len__(self):
		return len(self.coords)

	def __getitem__(self, n):
		return self.coords[n]

	def __str__(self):
		return str(self.coords)

	def norm(self):
		return sqrt(self*self)



def dist(v, w):
	if not iterable(v) or not iterable(w) or len(v) != len(w):
		raise TypeError('Vectors must be iterable, of length 2')
	
	u = Vector(v) - Vector(w)
	return u.norm()

def left_perpendicular(vector):
	if not iterable(vector) or len(vector) != 2:
		raise TypeError("Argument 'vector' must be iterable, of length 2")

	return Vector((-vector[1], vector[0]))

def right_perpendicular(vector):
	if not iterable(vector) or len(vector) != 2:
		raise TypeError("Argument 'vector' must be iterable, of length 2")

	return Vector((vector[1], -vector[0]))


def find_circles(v, w, radius, type='open'):

	if not iterable(v) or not iterable(w) or len(v) != len(w):
		raise TypeError('Vectors must be iterable, of length 2')

	try:
		float(radius)
		if radius < 0:
				raise TypeError(
					"Argument 'radius' must be greater or equal to 0"
				)
	except TypeError:
		raise TypeError("Argument 'radius' must be a number")

	distance = dist(v, w)
	if distance > 2*radius:
		return None

	pointer = (1 / 2)*(Vector(w) - Vector(v))
	
	d = pointer.norm()
	h = sqrt(abs(radius**2 - (d**2)))

	if type == 'open':
		res_left = Circle(
			Vector(v) + pointer + (h / d)*left_perpendicular(pointer), radius
		)
		res_right = Circle(
			Vector(v) + pointer + (h / d)*right_perpendicular(pointer), radius
		)
	
	elif type == 'closed':
		res_left = ClosedCircle(
			Vector(v) + pointer + (h / d)*left_perpendicular(pointer), radius
		)
		res_right = ClosedCircle(
			Vector(v) + pointer + (h / d)*right_perpendicular(pointer), radius
		)

	return (res_left, res_right)


if __name__ == '__main__':
	import matplotlib.pyplot as plt

	v = Vector([0, 0])
	w = Vector([1.2, 1])

	radius = 2

	circle_v = plt.Circle(v, radius, alpha=0.2)
	circle_w = plt.Circle(w, radius, alpha=0.2)

	fig, ax = plt.subplots()

	ax.add_artist(circle_v)
	ax.add_artist(circle_w)

	p = find_circles(v, w, radius)[0].center
	q = find_circles(v, w, radius)[1].center

	xs = [v[0], w[0], p[0], q[0]]
	ys = [v[1], w[1], p[1], q[1]]
	ax.scatter(xs, ys)


	plt.ylim(-2, 2)
	plt.xlim(-2, 2)
	plt.show()