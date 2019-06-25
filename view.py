from random import uniform

import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox

from graph import SpecialGraph


class View():

	def __init__(self):

		#Set default parameters
		self.yrange = 10
		self.xrange = 10
		self.n = 100
		
		self.elapsed = None
		self.num_colors = 0

		#Chose random colors
		self.colors_set = [uniform(0, 1) for i in range(self.n)]

		#
		fig, ax = plt.subplots()
		self.fig = fig
		self.ax = ax

		#Set limits to the subplot
		self.ax.set_ylim(0, self.yrange)
		self.ax.set_xlim(0, self.xrange)


		#Create buttons
		self.axbox_new = plt.axes([0, 0.95, 0.3, 0.05])
		self.button_new = Button(self.axbox_new, 'New Random Graph')
		self.button_new.on_clicked(self.new_graph)

		self.axbox_d = plt.axes([0.3, 0.95, 0.1, 0.05])
		self.button_d = Button(self.axbox_d, 'DSatur')
		self.button_d.on_clicked(self.on_click_d)

		self.axbox_gis = plt.axes([0.4, 0.95, 0.1, 0.05])
		self.button_gis = Button(self.axbox_gis, 'GIS')
		self.button_gis.on_clicked(self.on_click_gis)

		self.axbox_gis2 = plt.axes([0.5, 0.95, 0.1, 0.05])
		self.button_gis2 = Button(self.axbox_gis2, 'GISbis')
		self.button_gis2.on_clicked(self.on_click_gisbis)

		self.axbox_turbo = plt.axes([0.6, 0.95, 0.2, 0.05])
		self.button_turbo = Button(self.axbox_turbo, 'TURBOColor3000')
		self.button_turbo.on_clicked(self.on_click_turbo)

		self.axbox_col = plt.axes([0.8, 0.95, 0.2, 0.05])
		self.button_col = Button(self.axbox_col, 'Change Colors')
		self.button_col.on_clicked(self.on_click_col)

		#Create textboxes
		self.axbox_n = plt.axes([0.5, 0.9, 0.1, 0.05])
		self.textbox_n = TextBox(self.axbox_n, 'No. vertices:')
		self.textbox_n.on_submit(self.on_submit_n)

		self.axbox_y = plt.axes([0.7, 0.9, 0.1, 0.05])
		self.textbox_y = TextBox(self.axbox_y, 'yrange:')
		self.textbox_y.on_submit(self.on_submit_yrange)

		self.axbox_x = plt.axes([0.9, 0.9, 0.1, 0.05])
		self.textbox_x = TextBox(self.axbox_x, 'xrange:')
		self.textbox_x.on_submit(self.on_submit_xrange)

		#Adjust subplot
		plt.subplots_adjust(left=0.1, right=0.8)


	def draw(self):
		"""Draws a graph"""

		self.ax.clear()

		#Draw vertices
		xs = []
		ys = []
		colors = []
		for i in range(self.graph.ver_len()):
			vertex = self.graph[i]

			xs.append(vertex[0])
			ys.append(vertex[1])

			color_num = self.graph.colors[i]

			if color_num is None:
				colors.append('k')
			else:
				colors.append(self.colors_set[color_num])

		self.ax.scatter(xs, ys, c=colors)

		#Calculate the level of edges' transparency
		try:
			alpha = self.graph.edg_len()**(-0.4)
		except ZeroDivisionError:
			alpha = 1

		#Draw edges
		for edge in self.graph.edges:
			xs = [v[0] for v in edge]
			ys = [v[1] for v in edge]
			self.ax.plot(xs, ys, color='k', alpha=alpha)

		#Set lomits to the subplot
		self.ax.set_ylim(0, self.yrange)
		self.ax.set_xlim(0, self.xrange)


		#Show parameters and results
		try:
			el = str(round(self.elapsed, 5)) + 's'
		except TypeError:
			el = ''

		annotation = 'Vertices: {}\nColors: {}\nElapsed: \n{}'.\
			format(self.n, self.num_colors, el)

		self.ax.annotate(annotation, xy=(1.02, 0),xycoords='axes fraction',
             fontsize=10)


	def new_graph(self, event):
		"""Creates a new random graph"""

		xs = [uniform(0, self.xrange) for i in range(self.n)]
		ys = [uniform(0, self.yrange) for i in range(self.n)]

		vertices = [(xs[i], ys[i]) for i in range(self.n)]

		self.graph = SpecialGraph(vertices)
		self.draw()


	def on_click_d(self, event):
		"""Colors the graph using DSatur algorithm"""

		self.elapsed = self.graph.d_satur()
		self.graph.check_colors()

		self.num_colors = self.graph.num_colors()
		
		print('colors:', self.num_colors)
		self.draw()


	def on_click_gis(self, event):
		"""Colors the graph using GIS algorithm"""

		self.elapsed = self.graph.gis()
		self.graph.check_colors()

		self.num_colors = self.graph.num_colors()

		print('colors:', self.num_colors)
		self.draw()


	
	def on_click_gisbis(self, event):
		"""Colors the graph using GISbis algorithm"""
		
		self.elapsed = self.graph.gis_bis()
		self.graph.check_colors()

		self.num_colors = self.graph.num_colors()

		print('colors:', self.num_colors)
		self.draw()


	def on_click_turbo(self, event):
		"""Colors the graph using TURBOCOLOR3000 algorithm"""
		
		self.elapsed = self.graph.turbo_color_3000()
		self.graph.check_colors()

		self.num_colors = self.graph.num_colors()
		
		print('colors:', self.num_colors)
		self.draw()


	def on_click_col(self, event):
		"""Changes the set of colors"""

		self.colors_set = [uniform(0, 1) for i in range(self.n)]
		self.draw()

	def on_submit_n(self, text):
		"""Sets number of vertices"""

		try:
			if int(text) > 0:
				self.n = int(text)
			else:
				print('Entered value must be an integer greater then 0')

		except TypeError:
			print('Entered value must be an integer greater then 0')

	def on_submit_xrange(self, text):
		"""Sets range of the 'x' axis"""

		try:
			if float(text) > 0:
				self.xrange = float(text)
				self.ax.set_xlim(0, self.xrange)

			else:
				print('Entered value must be an number greater then 0')

		except TypeError:
			print('Entered value must be an number greater then 0')

	def on_submit_yrange(self, text):
		"""Sets range of the 'y' axis"""
		
		try:
			if float(text) > 0:
				self.yrange = float(text)
				self.ax.set_ylim(0, self.yrange)

			else:
				print('Entered value must be an number greater then 0')

		except TypeError:
			print('Entered value must be an number greater then 0')


if __name__ == '__main__':

	view = View()

	plt.show()