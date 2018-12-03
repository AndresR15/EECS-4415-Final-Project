import requests
import csv
import io
import sys

category = 0
catnum = 0;
catname = 1;
catdict = {}

numc = len(sys.argv)
if numc < 3:
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
		test = row.split(":")
		outstr = catdict[test[category]]
		for i in range(1, len(test)):
			outstr = outstr + ":" + test[i].replace("\n","")
		print(outstr)