import requests
import csv
import io
import sys

category = 0
catnum = 0;
catname = 1;
catdict = {}

numc = len(sys.argv)
if numc < 2:
	print("not enough parameters\n")
	sys.exit()
filename = sys.argv[1]
catfilename = sys.argv[2]

with io.open(catfilename, newline='', encoding='utf-8') as categories:
	csvReader = csv.reader(categories)
	next(csvReader,None)
	for row in csvReader:
		catdict[row[catnum]] = row[catname]
		
with io.open(filename, newline='', encoding='utf-8') as data:
	for row in data:
		test = row.split()
		outstr = catdict[test[category]]
		if len(test[0]) == 1:
			outstr = outstr + " "
		for i in range(2, len(row) - 1):
			outstr = outstr + row[i]
		print(outstr)