import requests
import csv
import io
import sys
from textblob import TextBlob

id = 3
title = 1
category = 0
desc = 2
ccat = '-1'
titlesent = [0,0,0]
descsent = [0,0,0]
numc = len(sys.argv)
if numc < 1:
	print("not enough parameters\n")
	sys.exit()
filename = sys.argv[1]

with io.open(filename, newline='', encoding='utf-8') as videos:
	csvReader = csv.reader(videos)
	for row in csvReader:
		if ccat == '-1':
			ccat = row[category]
		if ccat != row[category]:
			print(ccat + " " + str(titlesent) + " " + str(descsent))
			ccat = row[category]
			titlesent = [0,0,0]
			descsent = [0,0,0]
		
		if row[title] == '1':
			titlesent[0] = titlesent[0] + 1
		if row[title] == '0':
			titlesent[1] = titlesent[1] + 1
		if row[title] == '-1':
			titlesent[2] = titlesent[2] + 1
		
		if row[desc] == '1':
			descsent[0] = descsent[0] + 1
		if row[desc] == '0':
			descsent[1] = descsent[1] + 1
		if row[desc] == '-1':
			descsent[2] = descsent[2] + 1

print(ccat + " " + str(titlesent) + " " + str(descsent))