import sys

def printTable(B, fn, table, ZjCj=[], theta=[]):
	print
	print "\t|C\t",
	for i in fn:
		print str(i) + "\t",
	print
	print "-------",
	print "-------",
	for i in fn:
		print "-------",
	print

	print "B\t|X\t",
	for i in xrange(0, len(fn)):
		print str(i+1) + "\t",
	print
	print "-------",
	print "-------",
	for i in xrange(0, len(fn)):
		print "-------",
	print

	for rowNo in xrange(0, len(table)):
		print str(B[rowNo]+1) + "\t|",
		for i in table[rowNo]:
			print str(i) + "\t",
		if(len(theta) > 0): print "|" + str(theta[rowNo]),
		print

	if(len(ZjCj) > 0):
		print "-------",
		for i in ZjCj:
			print "-------",
		print
		print "Zj-Cj\t|",
		for i in ZjCj:
			print str(i) + "\t",
		print

	print
	print

def min_nonNeg(lst):
	min = -1;
	for i in lst:
		if(i > 0):
			if(min < 0):
				min = i
			else:
				if(i < min): min = i
	return min

def iterate(ZjCj, table, B, fn):	
	
	enteringCol = ZjCj.index(min(ZjCj[1:len(ZjCj)]))

	print "Entering Column: " + str(enteringCol);

	theta = []
	for row in table:
		if(row[enteringCol] != 0):
			theta.append(row[0] / row[enteringCol])
		else:
			theta.append(float("inf"))

	printTable(B, fn, table, ZjCj, theta)

	leavingRow = theta.index(min_nonNeg(theta))

	if(leavingRow < 0):
		print("ERROR: No Theta is positive!")
		sys.exit(1)

	print "Leaving Row: " + str(leavingRow+1);

	pivotElement = table[leavingRow][enteringCol]
	pivotEquation = [i/pivotElement for i in table[leavingRow]]

	print "Pivot Element: " + str(pivotElement) + " (" + str(leavingRow+1) + ", " + str(enteringCol) + ")";
	
	B[leavingRow] = enteringCol-1

	for row in table:
		newRow = []
		if(table.index(row) != leavingRow):
			for i in xrange(0, len(row)):
				newRow.append(row[i] - (row[enteringCol] * pivotEquation[i]))
		else:
			newRow = pivotEquation
		table[table.index(row)] = newRow

def isOptimum(fn, B, table):
	ZjCj = []
	for i in xrange(0, len(table[0])):
		Zj = 0
		for j in xrange(0, len(table)):
			Zj += (table[j][i] * fn[B[j]])
		ZjCj.append(Zj - fn[i-1])
	
	if(len([i for i in ZjCj[1:len(ZjCj)] if i >= 0]) == len(ZjCj[1:len(ZjCj)])):
		printTable(B, fn, table, ZjCj)
		global noVars
		global noCons
		if(ZjCj[0]<0):
			print "\nPseudo Optimum!!!"
		else:
			print "\nOptimum!"
		return [True, ZjCj]
	else:
		printTable(B, fn, table, ZjCj)
		print "\nNot Optimum!"
		return [False, ZjCj]

def eval_table(fn, B, table):
	check = isOptimum(fn, B, table)
	ct = 0
	while(check[0] == False):
		ct += 1
		print "________________________________________________________________________________________________________________________________"
		print "\nIteration " + str(ct) + ": -\n"
		iterate(check[1], table, B, fn)
		check = isOptimum(fn, B, table)
		print "________________________________________________________________________________________________________________________________"

	return check[1][0];