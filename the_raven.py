import os, re, copy, traceback
os.system('cls')
with open('a_raven.ascii', 'r') as intro: print intro.read()
raw_input("Press ENTER to continue...")
os.system('cls')

weights = {'shape':7,
		   'size':6,
		   'inside':2,
		   'fill':7,
		   'above':4,
		   'overlaps':3,
		   'angle':6,
		   'left-of':4,
		   'horizontal-flip':6,
		   'vertical-flip':6}

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
			#print "Adding Property " + "\"" + stripped + "\""
			f.properties[stripped[:colon]] = stripped[colon + 1 :]
		else:
			#print "Saving Figure " + f.name + " to picture " + picture.name
			picture.add_figure(f)
			f = Figure(line[1])
	return picture

def weigh_figures_transformations(f1, f2):
	weight = 0
	for p in f1.properties:
		if p in f2.properties:
			if f1.properties[p] == f2.properties[p]:
				weight += weights[p]
			else:
				weight -= weights[p]
		else:
			weight -= weights[p]
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

def relate_figures(weights,f1,f2):
	k1 = f1.figure_list.keys()
	k2 = f2.figure_list.keys()
	figures_relations = {}
	for figure in k1:
		figures_relations[figure] = ''
	while len(weights):
		relation = two_dim_max(weights)
		figures_relations[k1[relation[1]]] = k2[relation[0]]
		del(k1[relation[1]])
		del(k2[relation[0]])
		del(weights[relation[0]])
		for index, val in enumerate(weights):
			del(weights[index][relation[1]])
	return figures_relations

def weigh_pictures_transformations(p1,p2):
	p1_figures = p1.figure_list.keys()
	p2_figures = p2.figure_list.keys()
	weights = [['' for x in p1_figures]
	               for x in p2_figures]
	for col, col_name in enumerate(p1_figures):
		for row, row_name in enumerate(p2_figures):
			weights[row][col] = weigh_figures_transformations(p1.figure_list[p1_figures[col]],
			                                                  p2.figure_list[p2_figures[row]])
	return weights

def apply_transformations(p, template, relations):
	option = Picture()
	for old_figure_name, old_figure in p.figure_list.iteritems():
		new_name = relations[old_figure_name]
		transformations = template[new_name]
		if transformations != 'figure_deleted':
			figure = Figure(new_name)
			for new_key, new_value in transformations.iteritems():
				if new_value == 'same':
					#print old_figure.properties
					hey = old_figure.properties[new_key]
					figure.properties[new_key] = hey
				elif not new_value == 'deleted':
					figure.properties[new_key] = new_value
			option.add_figure(figure)
	return option

def compare_figures(f1,f2):
	are_they_equal = True
	for p1, v1 in f1.properties.iteritems():
		if p1 in f2.properties:
			if f2.properties[p1] == v1:
				are_they_equal &= True
			else:
				are_they_equal &= False
		else:
			are_they_equal &= False
	return 10 if are_they_equal else -10

def compare_pictures(p1,p2):
	weight = 0
	for p1_name, f1 in p1.figure_list.iteritems():
		for p2_name, f2 in p2.figure_list.iteritems():
			f2_copy = copy.deepcopy(f2)
			weight += compare_figures(f1,f2)
	return weight

solutions = []
corrects = []
for x in range(1,21): #Change this to (1,21) in final version
	print "Loading problem %02d..." % (x,)
	try:
		with open('Problems/2x1BasicProblem%02d.txt' % (x,), 'r') as p:
			lines = list(p)
			corrects.append(int(lines[2][0]))
			lines.append("\n,")
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
			#print a,b,c,s1,s2,s3,s4,s6

			# Generate figure relations list between pictures A and B
			a_b_transformations_weights = weigh_pictures_transformations(a,b)
			a_b_figures_relations = relate_figures(a_b_transformations_weights,a,b)
			#print a_b_figures_relations

			# Generate transformation template
			transformations_template = {}
			for index, relation in enumerate(a_b_figures_relations.iteritems()):
				old = relation[0]
				new = relation[1]
				transformations_template[old] = {}
				if new in b.figure_list:
					for p, a_v in a.figure_list[old].properties.iteritems():
						if p in b.figure_list[new].properties:
							b_v = b.figure_list[new].properties[p]
							if a_v == b_v:
								transformations_template[old][p] = 'same'
							else:
								transformations_template[old][p] = b_v
						else:
							transformations_template[old][p] = 'deleted'
				else:
					transformations_template[old] = 'figure_deleted'

			# Add 'added' properties to the transformation template
			for name, figure in b.figure_list.iteritems():
				for p, v in figure.properties.iteritems():
					if not p in transformations_template[name]:
						transformations_template[name][p] = v
			#print transformations_template

			# Generate figure relations list between pictures A and C
			a_c_transformations_weights = weigh_pictures_transformations(c,a)
			a_c_figures_relations = relate_figures(a_c_transformations_weights,c,a)
			#print a_c_figures_relations

			# Apply transformations template to C
			option = apply_transformations(c, transformations_template, a_c_figures_relations)
			#print option

			# Compare and weigh option with numbered possible solutions
			solution_weights = []
			s = [s1,s2,s3,s4,s5,s6]
			for i, solution in enumerate(s):
				solution_weights.append(compare_pictures(option, solution))
			#print solution_weights

			solutions.append(solution_weights.index(max(solution_weights))+1)
	except:
		print traceback.format_exc()
		solutions.append(0)
print solutions
print corrects