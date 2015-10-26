import os, re
os.system('cls')
with open('a_raven.ascii', 'r') as intro: print intro.read()
raw_input("Press ENTER to continue...")
os.system('cls')

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
	print f1.name
	print f2.name
	return 90

for x in range(5,6): #Change this to (1,21) in final version
	print "Loading problem %02d..." % (x,)
	with open('Problems/2x1BasicProblem%02d.txt' % (x,), 'r') as p:
		lines = list(p)
		lines.append("\n,")
		print lines
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
		a_figures = a.figure_list.keys()
		b_figures = b.figure_list.keys()
		possible_transformations = [['' for x in a_figures]
		                                for x in b_figures]
		print possible_transformations
		for col, col_name in enumerate(a_figures):
			for row, row_name in enumerate(b_figures):
				print '' + str(col) + ',' + str(row) + ':' 
				possible_transformations[row][col] = weigh_transformations(a.figure_list[a_figures[col]],
				                                                           b.figure_list[b_figures[row]])

		print possible_transformations