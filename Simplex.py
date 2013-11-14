from decimal import *

import table_funcs

inputFile = open('input.txt', 'r')

noVars, noCons = [int(x) for x in inputFile.readline().split()]

inputFile.readline()

whatToDo = inputFile.readline()

fn = [Decimal(x) for x in inputFile.readline().split()]
if(whatToDo=='Min\n'):
	for i in xrange(0, len(fn)):
		fn[i] = -1*fn[i]


inputFile.readline()

cons = []
consSymbols = []
for i in xrange(0, noCons):
	temp =  [x for x in inputFile.readline().split()]
	cons.append([Decimal(x) for x in temp[0:(noVars+1)]])
	consSymbols.append(temp[noVars+1])

# -- Got Input -- #

slackVars = []
for i in xrange(0, len(cons)):
	if(consSymbols[i] == '<='):
		slackVars.append(cons[i][noVars]) # Initial Basic Feasible Solution, Slack Variables = Constants
	fn.append(Decimal('0'));

M = 100;

artificialVars = []
for i in xrange(0, len(cons)):
	if(consSymbols[i] != '<='):
		artificialVars.append(cons[i][noVars]) # Initial Basic Feasible Solution, Slack Variables = Constants
		fn.append(Decimal(-1*Decimal(M)));

B = []
ct_Slack = 0
ct_Artificial = 0
for i in xrange(0, len(cons)):
	if(consSymbols[i] == '<='):
		B.append(noVars+ct_Slack)
		ct_Slack += 1
	elif(consSymbols[i] != '<='):
		B.append(noVars+noCons+ct_Artificial)
		ct_Artificial += 1

expandedCons = []
ct_Slack = 0
ct_Artificial = 0
for i in xrange(0, noCons):
	temp1 = cons[i][:len(cons[i])-1]

	if(consSymbols[i] == '<='):
		temp1.insert(0, slackVars[ct_Slack])
		ct_Slack += 1
	elif(consSymbols[i] != '<='):
		temp1.insert(0, artificialVars[ct_Artificial])
		ct_Artificial += 1

	temp2 = [Decimal(0)] * (len(fn)-noVars);

	if(consSymbols[i] == '<='):
		temp2[i] = Decimal('1')
	elif(consSymbols[i] != '<='):
		temp2[i] = Decimal('-1')
		temp2[noCons+ct_Artificial-1] = Decimal('1')

	temp1.extend(temp2)

	expandedCons.append(temp1)

table = expandedCons

result = table_funcs.eval_table(fn, B, table)

res = 0
varValues = [0] * noVars
for rowNo in xrange(0, len(table)):
	if(B[rowNo] < noVars):
		varValues[B[rowNo]] = table[rowNo][0]
		res += varValues[B[rowNo]] * fn[B[rowNo]]

if(whatToDo=='Min\n'):
	print "Minimum",
else:
	print "Maximum",
print "value of function: " + str(res) + "\n"

for i in xrange(0, noVars):
	print "\tVar " + str(i+1) + ": " + str(varValues[i])