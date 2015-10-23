import os
os.system('cls')
with open('a_raven.ascii', 'r') as f:
	print f.read()

raw_input("Press ENTER to continue...")
os.system('cls')
for x in range(1,2): #Change this to (1,21) in final version
	print "Loading problem %02d" % (x,)
	with open('Problems/2x1BasicProblem%02d.txt' % (x,), 'r') as p:
		print p.read()