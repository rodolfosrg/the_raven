import os, re
os.system('cls')
with open('a_raven.ascii', 'r') as intro: print intro.read()
raw_input("Press ENTER to continue...")
os.system('cls')

weights = {'shape':9,
		   'size':3,
		   'inside':2,
		   'fill':8,
		   'above':4,
		   'overlaps':3,
		   'angle':7,
		   'left-of':4,
		   'horizontal-flip':8,
		   'vertical-flip':8}

class Figure(object):
	def __init__(self,name):
		self.name = name
		self.properties = {}
	def __str__(self):
		out = ""
		for key, value in self.properties.iteritems():
			out += key + ":" + value + "\r\n"
		return out
	str = __str__
	__rep__=__str__

class Picture(object):
	def __init__(self):
		self.name = ''
		self.figure_list = {}
	def add_figure(self,figure):
		self.figure_list[figure.name] = figure
	def __str__(self):
		out = self.name + "\r\n"
		for key, value in self.figure_list.iteritems():
			out += key + "\r\n"
			out += value.str()
		return out

def parse_picture(lines, start, finish):
	picture = Picture()
	picture.name = lines[start][0]
	f = Figure(lines[start + 1][1])
	for line in lines[start + 2 : finish + 1]:
		#print line[:-1]
		if line[:2] == "\t\t":
			stripped = line[2:].replace('\n','').replace('\r','')
			colon = stripped.find(':')
			print "Adding Property " + "\"" + stripped + "\""
			f.properties[stripped[:colon]] = stripped[colon + 1 :]
		else:
			print "Saving Figure " + f.name + " to picture " + picture.name
			picture.add_figure(f)
			f = Figure(line[1])
	return picture

def weigh_transformations(f1, f2):
	print f1
	print f2
	weight = 0
	for p in f1.properties:
		if p in f2.properties:
			if f1.properties[p] == f2.properties[p]:
				weight += weights[p]
			else:
				weight -= weights[p]
		else:
			weight -= weights[p]
	print weight
	return weight

def two_dim_max(matrix):
	largest = -500
	for i, v in enumerate(matrix):
		candidate = max(v)
		if candidate > largest:
			largest = candidate
			row = i
			column = v.index(largest)
	return row, column

for x in range(12,13): #Change this to (1,21) in final version
	print "Loading problem %02d..." % (x,)
	with open('Problems/2x1BasicProblem%02d.txt' % (x,), 'r') as p:
		lines = list(p)
		lines.append("\n,")
		print lines
		# Parse pictures into Picture/Figure structures
		for index, line in enumerate(lines[3:]):
			if line[0] == 'A': index_a = index + 3
			if line[0] == 'B': index_b = index + 3
			if line[0] == 'C': index_c = index + 3
			if line[0] == '1': index_s1 = index + 3
			if line[0] == '2': index_s2 = index + 3
			if line[0] == '3': index_s3 = index + 3
			if line[0] == '4': index_s4 = index + 3
			if line[0] == '5': index_s5 = index + 3
			if line[0] == '6': index_s6 = index + 3
		a = parse_picture(lines, index_a, index_b)
		b = parse_picture(lines, index_b, index_c)
		c = parse_picture(lines, index_c, index_s1)
		s1 = parse_picture(lines, index_s1, index_s2)
		s2 = parse_picture(lines, index_s2, index_s3)
		s3 = parse_picture(lines, index_s3, index_s4)
		s4 = parse_picture(lines, index_s4, index_s5)
		s5 = parse_picture(lines, index_s5, index_s6)
		s6 = parse_picture(lines, index_s6, len(lines))
		print a,b,c,s1,s2,s3,s4,s6

		# Generate transformation weights matrix
		a_figures = a.figure_list.keys()
		b_figures = b.figure_list.keys()
		transformations_weights = [['' for x in a_figures]
		                                for x in b_figures]
		for col, col_name in enumerate(a_figures):
			for row, row_name in enumerate(b_figures):
				print '' + str(col) + ',' + str(row) + ':' 
				transformations_weights[row][col] = weigh_transformations(a.figure_list[a_figures[col]],
				                                                          b.figure_list[b_figures[row]])
		print transformations_weights

		# Generate figure relations list
		figure_relations = {}
		for figure in a_figures:
			figure_relations[figure] = ''
		while len(transformations_weights):
			relation = two_dim_max(transformations_weights)
			figure_relations[a_figures[relation[1]]] = b_figures[relation[0]]
			print a_figures[relation[1]], b_figures[relation[0]]
			del(a_figures[relation[1]])
			del(b_figures[relation[0]])
			del(transformations_weights[relation[0]])
			for index, val in enumerate(transformations_weights):
				del(transformations_weights[index][relation[1]])
			print transformations_weights
		print figure_relations	