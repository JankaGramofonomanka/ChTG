import time

from geometry import Circle, ClosedCircle, dist, find_circles
from misc import (
	iterable, between, always_true
)

class Graph():
	"""A class to represent a graph"""

	def cond(self, edge):
		"""This is a condition that must be satisfied by an edge to be included 
		in creating a graph 
		The condition will be modified in classes that inherit from this class
		"""
		if iterable(edge) and len(edge) == 2:
			ed_list = list(edge)
			
			if (
				ed_list[0] != ed_list[1]
				and ed_list[0] in self.vertices 
				and ed_list[1] in self.vertices
			):
				return True
			
			else:
				return False
		else:
			return False



	
	def __init__(self, vertices, edges=None):

		try:
			iter(vertices)
		except TypeError:
			raise TypeError("Argument 'vertices' must be iterable")

		#Remove redundant vertices
		self.vertices = list(set(vertices))

		#If edges are not passed all possible edges will be added to the graph
		if edges is None:
			edges = []
			for v in self.vertices:
				for w in self.vertices:
					if v == w:
						continue

					edges.append({v, w})

		try:
			iter(edges)
		except TypeError:
			edges = []


		#Add all edges that satisfy the condition 'self.cond'
		self.edges = []
		for edge in edges:
			if self.cond(edge) and edge not in self.edges:
				self.edges.append(set(edge))

		#Initialize a list of colors
		self.colors = [None for  v in self.vertices]



	def are_neighbors(self, v, w):
		"""Returns True if v and w are neighbors, False otherwise"""
		return {v, w} in self.edges



	def ver_len(self):
		"""Returns the numbr of vertices"""
		return len(self.vertices)

	def edg_len(self):
		"""Returns the number of edges"""
		return len(self.edges)

	def __getitem__(self, n):
		"""Returns the n-th vertice"""
		return self.vertices[n]

	
	def __sub__(self, other):
		"""Returns a graph that is formed by removing vertices given in 'other' 
		argument"""

		if not iterable(other):
			other = [oher]

		vertices = self.vertices.copy()
		for v in other:
			vertices.remove(v)

		"""If 'self' is an instance of a class that inherits from 'Graph', an 
		instance of the same class will be returned"""
		return type(self)(vertices, self.edges)

	def remove(self, v):
		"""Removes a vertice from a graph"""

		if v in self.vertices:
			self.vertices.remove(v)
		for edge in self.edges:
			if v in edge:
				self.edges.remove(edge)

	def remove_set(self, removed):
		"""Removes a set of vertices from a graph"""

		for v in removed:
			if v in self.vertices:
				self.vertices.remove(v)
		for edge in self.edges:
			rem = False
			for v in edge:
				if v in removed:
					rem = True
			if rem:
				self.edges.remove(edge)

	def copy(self):
		"""Returns a graph identical to 'self'"""
		GraphType = type(self)
		return GraphType(self.vertices, self.edges)

	def deg(self, v):
		"""Returns number of neighbors of 'v'"""
		if type(v) == int and between(-1, v, self.ver_len()):
			v = self[v]

		if v not in self.vertices:
			raise ValueError('Argument must be a vertex of the graph')

		deg = 0

		"""
		for w in self.vertices:
			if self.are_neighbors(v, w):
				deg += 1
		"""
		for edge in self.edges:
			if v in edge:
				deg += 1
		#"""

		return deg

	def get_max_ver(self):
		"""Returns a vertice that has the biggest number of neighbors"""
		v = self[0]
		for w in self.vertices:
			if self.deg(v) < self.deg(w):
				v = w
		return v

	def get_min_ver(self):
		"""Returns a vertice that has the smallest number of neighbors"""
		v = self[0]
		for w in self.vertices:
			if self.deg(v) > self.deg(w):
				v = w
		return v

	def check_colors(self):
		"""Returns True if a graph is colored properly, that is no two neighbors 
		have the same color, False otherwise"""
		
		for v in self.vertices:
			i = self.vertices.index(v)
			for w in self. vertices:
				j = self.vertices.index(w)
				if (
					self.are_neighbors(v, w) 
					and self.colors[i] == self.colors[j]
				):
					print('Bad colors :(')
					print('vertices:', v, w)
					print('dist:', dist(v, w))
					print('colors:', self.colors[i], self.colors[j])
					return False

		print('Good colors :)')
		return True

	def num_colors(self):
		"""Returns the number of colors used in coloring of a graph"""
		return len(set(self.colors))


	def get_neighbors(self, v, cond=always_true):
		"""Returns a list of neighbors that satisfy the condition 'cond' given 
		as an argument
		If a condition is not given, all neighbors will be returned"""
		
		if type(v) == int and between(-1, v, self.ver_len()):
			v = self[v]

		if v not in self.vertices:
			raise ValueError('Argument must be a vertex of the graph')

		neighbors = []
		for w in self.vertices:
			if self.are_neighbors(v, w) and cond(w):
				neighbors.append(w)

		return neighbors

	def is_colored_func(self):
		"""Returns a function that returns True if its argument is a colored 
		vertice of 'self', False otherwise"""
		def func(v):
			if v not in self.vertices:
				return False

			i = self.vertices.index(v)
			return self.colors[i] is not None

		return func
	
	def get_neighbors_colors(self, v):
		"""Returns a list of colors assigned to neighbors of 'v'"""
		colors = []
		for w in self.get_neighbors(v):
			i = self.vertices.index(w)
			if self.colors[i] is not None:
				colors.append(self.colors[i])

		return list(set(colors))


	def d_satur(self):
		"""Colors the graph according to the DSatur algorithm
		Returns time spent on executing it"""

		print('DSATUR')

		#Start counting time
		start = time.clock()

		#Erase existing colors 
		self.colors = [None for  v in self.vertices] 

		#Copy the graph
		graph = self.copy()

		#Let 'v' be a vertice of maximum degree
		v = self.get_max_ver() 

		#Assign to 'v' the color '0' 
		i = self.vertices.index(v)
		self.colors[i] = 0

		#Create a list of colored vertices
		colored = [v]

		#Remove 'v' from 'graph'
		graph.remove(v)

		"""'neighbors' will be a list of vertices that have at least one colored 
		neighbor"""
		neighbors = self.get_neighbors(v)

		while graph.ver_len() > 0:

			#Find a vertice whose neighbors have the biggest number of colors
			try:
				#'w' will be the vertice that we are looking for
				w = neighbors[0]
				neighbors_colors = self.get_neighbors_colors(w)
				
				"""'max_colors' will hold the number of colors assigned to 
				neighbors of 'w'"""
				max_colors = len(neighbors_colors)
				
				"""If any vertex has a higher number of colors assigned to it's 
				neighbors than 'w', chose it instead of 'w'"""
				for vertex in neighbors:

					neighbors_colors_vertex = self.get_neighbors_colors(vertex)

					num_colors = len(neighbors_colors_vertex)

					if num_colors > max_colors:
						w = vertex
						max_colors = num_colors


			except IndexError:
				#If 'neighbors' is empty chose any vertice
				w = graph[0] 

			#Assign to 'w' the smallest possible color
			neighbors_colors = self.get_neighbors_colors(w)

			w_color = 0
			while w_color in neighbors_colors:
				w_color += 1

			i = self.vertices.index(w)
			self.colors[i] = w_color

			#Add 'w' to the list of colored vertices
			colored.append(w)

			#and remove it from 'neighbors'
			if w in neighbors:
				neighbors.remove(w)
			
			#Add neighbors of 'w' to 'neighbors'
			w_neighbors = graph.get_neighbors(w)
			for vertex in w_neighbors:
				if vertex not in neighbors:
					neighbors.append(vertex)

			#Remove 'w' from 'graph'
			graph.remove(w)

		elapsed = time.clock() - start
		print('Elapsed:', elapsed)

		#Return time spent on coloring
		return elapsed



	def independent(self):
		"""Returns a maximal independent set
		(maximal means that no other independent set cantains it, 
		doesn't mean that it has the most vertices)"""

		if self.ver_len() == 0:
			return None
		else:
			#Let 'v' be a vertice of minimal degree
			#'v' will be added to the independent set
			v = self.get_min_ver() 

			#Remove neighbors of 'v'
			new_graph = self - (self.get_neighbors(v) + [v])
			
			#Repeat the action for the vertices that remained
			ind = new_graph.independent()

			if ind is not None:
				return [v] + ind
			return [v]
			
	def gis(self):
		"""Colors the graph according to the GIS algorithm
		Returns time spent on executing it"""

		print('GIS')

		#Start counting time
		start = time.clock() 

		#Erase existing colors 
		self.colors = [None for  v in self.vertices]

		#Let 'graph' be a copy of our graph
		graph = self.copy()

		#Let 'MIS' be a maximal independent set
		MIS = graph.independent()
		i = 1
		while MIS is not None:
			#Assign to "MIS's" vertices the 'i'-th color
			for v in MIS:
				self.colors[self.vertices.index(v)] = i
			
			#Remove 'MIS' from 'graph'
			graph.remove_set(MIS)

			i += 1
			
			#Repeat the action for what remained of 'graph'
			MIS = graph.independent()

		elapsed = time.clock() - start
		print('Elapsed:', elapsed)

		#Return time spent on coloring
		return elapsed





class SpecialGraph(Graph):
	"""A class to represent a graph with points on a surface as vertices, such 
	that every two vertices are connected with an edge only if distance between 
	them is between 1 and 2"""

	def cond(self, edge):
		"""This is a condition that must be satisfied by an edge to be included 
		in creating a graph 
		It says that distance between vertices connected by it must be between 
		1 and 2"""

		if Graph.cond(self, edge):
			v = list(edge)[0]
			w = list(edge)[1]
			return between(1, dist(v, w), 2)

		else:
			return False



	def __init__(self, vertices, edges=None):
		
		#Do everything needed to create an ordinary graph
		Graph.__init__(self, vertices, edges)

		#Check if vertices are points on a surface
		if len(vertices) >= 1:
			v = vertices[0]
			if not iterable(v) and len(v) != 2: 
				raise ValueError(
					"""Vertices (elements of 'vertices' argument) must be 
					iterable, of length 2"""
				)


	def are_neighbors(self, v, w):
		"""Returns True if v and w are neighbors, False otherwise"""
		return between(1, dist(v, w), 2)


	def turbo_independent(self):
		"""Returns a maximal independent set
		(maximal means that no other independent set cantains it, 
		doesn't mean that it has the most vertices)"""

		#Return 'None' if there are no vertices
		if self.ver_len() == 0:
			return None

		#Let 'v' be a vertice closest to (0, 0)
		v = self[0]
		dist_v = dist(v, (0, 0))
		for w in self.vertices:
			d = dist(w, (0, 0))
			if d < dist_v:
				v = w
				dist_v = d

		"""'close_circle' is now a circle with a center in 'v' and radius of 
		length 1, this means that no vertice contained in 'close_circle' is 
		connected with 'v'"""
		close_circle = Circle(v, 1)

		"""Let 'close_vertices' be a list containing vertices that lay in 
		'close_circle'"""
		close_vertices = []

		for w in self.vertices:
			if w in close_circle:
				close_vertices.append(w)

		"""'the_circle' will be a closed circle that will contain vertices 
		chosen as elements of returned set, it has to have diameter of length 1 
		so that no two vertices that lay in it are connected and it has to 
		contain 'v'
		
		'max_card' will be the number of those vertices"""
		max_card = 0
		the_circle = ClosedCircle(v, 0.5)
		
		#Count vertices in 'the_circle'
		for vertex in close_vertices:
			if vertex in the_circle:
				max_card += 1

		#We want 'the_circle' to contain the most vertices possible
		for w in close_vertices:
			if w == v:
				continue

			"""'circ_1' and 'circ_1' are closed circles with diameter of length 
			1, such that 'v' and 'w' lay on edges of 'circ_1' and 'circ_1'"""
			circles = find_circles(v, w, 0.5, type='closed')
			circ_1 = circles[0]
			circ_2 = circles[1]

			#'card_1' will be the number of vertices that lay in 'circ_1'
			card_1 = 0

			#Count vertices in 'circ_1'
			for vertex in close_vertices:
				if vertex in circ_1:
					card_1 += 1

			"""If 'circ_1' contains more vertices than 'the_ circle' swap them 
			with one another"""
			if card_1 > max_card:
				the_circle = circ_1
				max_card = card_1

			#'card_2' will be the number of vertices that lay in 'circ_2'
			card_2 = 0

			#Count vertices in 'circ_2'
			for vertex in close_vertices:
				if vertex in circ_2:
					card_2 += 1

			"""If 'circ_2' contains more vertices than 'the_ circle' swap them 
			with one another"""
			if card_2 > max_card:
				the_circle = circ_2
				max_card = card_2

		#'chosen_vertices' will be a list of all vertices from 'the_circle'
		chosen_vertices = []
		for w in close_vertices:
			if w in the_circle:
				chosen_vertices.append(w)

		"""'big_circle' is a circle that contains vertices that can be connected
		with vertices from 'the_circle'"""
		big_circle = Circle(the_circle.center, 2.5)

		#'rejested' will be a list of vertices from 'big_cirle'
		rejected = []
		for w in self.vertices:
			if w in big_circle:
				rejected.append(w)

		"""remove vertices from 'rejected' because it contains alredy chosen 
		vertices as well as their potential neighbors"""
		new_graph = self - rejected
		
		#Repeat the action for what remained
		ind = new_graph.turbo_independent()
		
		if ind is None:
			return chosen_vertices
		else:
			return ind + chosen_vertices



	
	def turbo_color_3000(self):
		"""Colors the graph according to the TURBOCOLOR3000 algorithm
		
		Returns time spent on executing it"""

		print('TURBOCOLOR3000')

		#Start counting time
		start = time.clock()

		#Erase existing colors 
		self.colors = [None for  v in self.vertices]

		#Let 'graph' be a copy of our graph
		graph = self.copy()

		#Let 'ind' be a maximal independent set
		ind = graph.turbo_independent()

		color = 0
		while ind is not None:
			#Assign to "ind's" vertices the 'i'-th color
			for w in ind:
				i = self.vertices.index(w)
				self.colors[i] = color
			
			#Remove 'ind' from 'graph'
			graph.remove_set(ind)

			color += 1

			#Repeat the action for what remained of 'graph'
			ind = graph.turbo_independent()

		elapsed = time.clock() - start
		print('Elapsed:', elapsed)
		
		#Return time spent on coloring
		return elapsed




	def independent_2(self):
		"""	Returns a maximal independent set
		(maximal means that no other independent set cantains it, 
		doesn't mean that it has the most vertices)"""

		if self.ver_len() == 0:
			return None
		else:
			#Let 'v' be a vertice closest to (0, 0)
			#'v' will be added to the independent set
			v = self[0]
			odle = dist(v, (0, 0))
			for w in self.vertices:
				if dist(w,(0,0)) < odle:
					odle = dist(w,(0,0))
					v = w

			#Remove neighbors of 'v'
			new_graph = self - (self.get_neighbors(v) + [v])
			
			#Repeat the action for the vertices that remained
			ind = new_graph.independent_2()

			if ind is not None:
				return [v] + ind
			return [v]	
			
	def gis_bis(self):
		"""Colors the graph according to the GIS algorithm with modified method 
		of finding a maximal independent set
		
		Returns time spent on executing it"""

		print('GISBIS')

		#Start counting time
		start = time.clock() 

		#Erase existing colors 
		self.colors = [None for  v in self.vertices]

		#Let 'graph' be a copy of our graph
		graph = self.copy()

		#Let 'MIS' be a maximal independent set
		MIS = graph.independent_2()
		i = 1
		while MIS is not None:
			
			#Assign to "MIS's" vertices the 'i'-th color
			for v in MIS:
				self.colors[self.vertices.index(v)] = i
			
			#Remove 'MIS' from 'graph'
			graph.remove_set(MIS)
			i = i + 1
			
			#Repeat the action for what remained of 'graph'
			MIS = graph.independent_2()

		elapsed = time.clock() - start
		print('Elapsed:', elapsed)

		#Return time spent on coloring
		return elapsed
		return elapsed


