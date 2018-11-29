import requests
import csv
import io
import sys

id = 0
category = 4
categories = []
catwvid = []

numc = len(sys.argv)
if numc < 1:
	print("not enough parameters\n")
	sys.exit()
filename = sys.argv[1]

with io.open(filename, newline='', encoding='utf-8') as videos:
	csvReader = csv.reader(videos)
	next(csvReader,None)
	for row in csvReader:
		var = row[category]
		vidid = row[id]
		if var not in categories and var is not "category_id":
			categories.append(var)
			catwvid.append([var,vidid])
categories.sort()
print(categories)
print(catwvid)