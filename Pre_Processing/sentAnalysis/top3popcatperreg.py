import requests
import csv
import io
import sys

id = 3
title = 1
category = 0
desc = 2
ccat = '-1'
catsum = 0
catdict = {}
numc = len(sys.argv)
if numc < 1:
	print("not enough parameters\n")
	sys.exit()
filename = sys.argv[1]

with io.open(filename, newline='', encoding='utf-8') as line:
	csvReader = csv.reader(line)
	for row in csvReader:
		if ccat == '-1':
			ccat = row[category]
		if ccat != row[category]:
			catdict[ccat] = catsum
			ccat = row[category]
			catsum = 0
		
		catsum = catsum + 1

# output string is catagory name, title sentiments, then description sentiments
catdict[ccat] = catsum
test = sorted(catdict.items(), key=lambda x: x[1])
for x in range(len(test) - 3, len(test)):
	print (test[x][0] + ":" + str(test[x][1]))