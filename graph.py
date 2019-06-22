import time

from geometry import Circle, ClosedCircle, dist, find_circles
from misc import (
	iterable, between, always_true
)

class Graph():

	def cond(self, edge):
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
		"""Konstruktor"""

		try:
			iter(vertices)
		except TypeError:
			raise TypeError("Argument 'vertices' must be iterable")

		self.vertices = list(set(vertices))

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


		self.edges = []
		for edge in edges:
			if self.cond(edge) and edge not in self.edges:
				self.edges.append(set(edge))

		self.colors = [None for  v in self.vertices]



	def are_neighbors(self, v, w):
		return {v, w} in self.edges



	def ver_len(self):
		return len(self.vertices)

	def edg_len(self):
		return len(self.edges)

	def __getitem__(self, n):
		"""przeciazony operator []"""
		return self.vertices[n]

	
	def __sub__(self, other):
		"""przeciazony operator - """

		if not iterable(other):
			other = [oher]

		vertices = self.vertices.copy()
		for v in other:
			vertices.remove(v)

		return type(self)(vertices, self.edges)

	def remove(self, v):

		if v in self.vertices:
			self.vertices.remove(v)
		for edge in self.edges:
			if v in edge:
				self.edges.remove(edge)

	def remove_set(self, removed):

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
		GraphType = type(self)
		return GraphType(self.vertices, self.edges)

	def deg(self, v):
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
		v = self[0]
		for w in self.vertices:
			if self.deg(v) < self.deg(w):
				v = w
		return v

	def get_min_ver(self):
		v = self[0]
		for w in self.vertices:
			if self.deg(v) > self.deg(w):
				v = w
		return v

	def check_colors(self):
		
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
		return len(set(self.colors))


	def get_neighbors(self, v, cond=always_true):		
		"""jezeli cond jest podany to get_neighbors zwraca liste takich w, ze w 
		jest sasaidem v i cond(w) == True"""
		
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
		def func(v):
			if v not in self.vertices:
				return False

			i = self.vertices.index(v)
			return self.colors[i] is not None

		return func
	
	def get_neighbors_colors(self, v):
		colors = []
		for w in self.get_neighbors(v):
			i = self.vertices.index(w)
			if self.colors[i] is not None:
				colors.append(self.colors[i])

		return list(set(colors))


	def d_satur(self):

		print('DSATUR')
		start = time.clock() 
		self.colors = [None for  v in self.vertices]

		graph = self.copy()

		v = self.get_max_ver()

		i = self.vertices.index(v)
		self.colors[i] = 0

		colored = [v]

		graph.remove(v)

		neighbors = self.get_neighbors(v)

		while graph.ver_len() > 0:

			"""Szukaj takiego wierzcholka ze liczba kolorów jego pokolorowanych 
			sasiadow jest najwieksza"""
			#"""
			try:
				w = neighbors[0]
				neighbors_colors = self.get_neighbors_colors(w)
				
				max_colors = len(neighbors_colors)
				
				for vertex in neighbors:

					neighbors_colors_vertex = self.get_neighbors_colors(vertex)

					num_colors = len(neighbors_colors_vertex)

					if num_colors > max_colors:
						w = vertex
						max_colors = num_colors


			except IndexError:
				w = graph[0]

			#i pokoloruj go na najmniejszy dostepny kolor
			neighbors_colors = self.get_neighbors_colors(w)

			w_color = 0
			while w_color in neighbors_colors:
				w_color += 1

			i = self.vertices.index(w)
			self.colors[i] = w_color

			#technikalia
			colored.append(w)
			if w in neighbors:
				neighbors.remove(w)
			w_neighbors = graph.get_neighbors(w)
			
			for vertex in w_neighbors:
				if vertex not in neighbors:
					neighbors.append(vertex)


			graph.remove(w)

		elapsed = time.clock() - start
		print('Elapsed:', elapsed)
		return elapsed



	def independent(self):
		
		if self.ver_len() == 0:
			return None
		else:
			v = self.get_min_ver() 
			new_graph = self - (self.get_neighbors(v) + [v])
			ind = new_graph.independent()
			if ind is not None:
				return [v] + ind
			return [v]
			
	def gis(self):

		print('GIS')
		start = time.clock() 
		self.colors = [None for  v in self.vertices]

		graph = self.copy()

		MIS = graph.independent()
		i = 1
		while MIS is not None:
			for v in MIS:
				self.colors[self.vertices.index(v)] = i
			
			graph.remove_set(MIS)

			i += 1
			
			MIS = graph.independent()

		elapsed = time.clock() - start
		print('Elapsed:', elapsed)
		return elapsed





class SpecialGraph(Graph):

	def cond(self, edge):
		if Graph.cond(self, edge):
			v = list(edge)[0]
			w = list(edge)[1]
			return between(1, dist(v, w), 2)

		else:
			return False



	def __init__(self, vertices, edges=None):
		
		Graph.__init__(self, vertices, edges)
		if len(vertices) >= 1:
			v = vertices[0]
			if not iterable(v) and len(v) != 2: 
				raise ValueError(
					"""Vertices (elements of 'vertices' argument) must be 
					iterable, of length 2"""
				)


	def are_neighbors(self, v, w):
		return between(1, dist(v, w), 2)


	def turbo_independent(self):
		if self.ver_len() == 0:
			return None

		#znajdz wierzcholek najblizej (0, 0)
		v = self[0]
		dist_v = dist(v, (0, 0))
		for w in self.vertices:
			d = dist(w, (0, 0))
			if d < dist_v:
				v = w
				dist_v = d

		#obracanie kolek:
		close_circle = Circle(v, 1)
		close_vertices = []

		for w in self.vertices:
			if w in close_circle:
				close_vertices.append(w)

		max_card = 0
		the_circle = ClosedCircle(v, 0.5)
		for vertex in close_vertices:
			if vertex in the_circle:
				max_card += 1

		for w in close_vertices:
			if w == v:
				continue

			circles = find_circles(v, w, 0.5, type='closed')
			circ_1 = circles[0]
			circ_2 = circles[1]

			card_1 = 0
			for vertex in close_vertices:
				if vertex in circ_1:
					card_1 += 1

			if card_1 > max_card:
				the_circle = circ_1
				max_card = card_1

			card_2 = 0			
			for vertex in close_vertices:
				if vertex in circ_2:
					card_2 += 1

			if card_2 > max_card:
				the_circle = circ_2
				max_card = card_2
		#koniec obracania


		chosen_vertices = []
		for w in close_vertices:
			if w in the_circle:
				chosen_vertices.append(w)

		big_circle = Circle(the_circle.center, 2.5)
		rejected = []
		for w in self.vertices:
			if w in big_circle:
				rejected.append(w)


		new_graph = self - rejected
		
		ind = new_graph.turbo_independent()
		
		if ind is None:
			return chosen_vertices
		else:
			return ind + chosen_vertices



	
	def turbo_color_3000(self):

		print('TURBOCOLOR3000')
		start = time.clock()
		self.colors = [None for  v in self.vertices]
	
		graph = self.copy()
		ind = graph.turbo_independent()

		color = 0
		while ind is not None:

			for w in ind:
				i = self.vertices.index(w)
				self.colors[i] = color
			
			graph.remove_set(ind)

			color += 1
			ind = graph.turbo_independent()

		elapsed = time.clock() - start
		print('Elapsed:', elapsed)
		return elapsed




	def independent_2(self):
		if self.ver_len() == 0:
			return None
		else:
			
			v = self[0]
			odle = dist(v, (0, 0))
			for w in self.vertices:
				if dist(w,(0,0)) < odle:
					odle = dist(w,(0,0))
					v = w	
			new_graph = self - (self.get_neighbors(v) + [v])
			ind = new_graph.independent_2()
			if ind is not None:
				return [v] + ind
			return [v]	
			
	def gis_bis(self):

		print('GISBIS')
		start = time.clock() 
		self.colors = [None for  v in self.vertices]

		graph = self.copy()
		MIS = graph.independent_2()
		i = 1
		while MIS is not None:
			for v in MIS:
				self.colors[self.vertices.index(v)] = i
			
			graph.remove_set(MIS)
			i = i + 1
			MIS = graph.independent_2()

		elapsed = time.clock() - start
		print('Elapsed:', elapsed)
		return elapsed


