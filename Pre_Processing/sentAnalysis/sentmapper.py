import requests
import csv
import io
import sys
from textblob import TextBlob

id = 0
title = 2
category = 4
desc = 15

numc = len(sys.argv)
if numc < 1:
	print("not enough parameters\n")
	sys.exit()
filename = sys.argv[1]

with io.open(filename, newline='', encoding='utf-8') as videos:
	csvReader = csv.reader(videos)
	next(csvReader,None)
	for row in csvReader:
		titsentval = 0;
		descsentval = 0;
		vidid = row[id]
		vidtit = row[title]
		vidcat = row[category]
		viddesc = row[desc]
		analysis = TextBlob(vidtit)
		if analysis.sentiment.polarity > 0: 
			titsentval = 1
		elif analysis.sentiment.polarity == 0: 
			titsentval = 0
		else: 
			titsentval = -1
		analysis = TextBlob(viddesc)
		if analysis.sentiment.polarity > 0: 
			descsentval = 1
		elif analysis.sentiment.polarity == 0: 
			descsentval = 0
		else: 
			descsentval = -1
		print(vidcat + "," + str(titsentval) + "," + str(descsentval) + "," + vidid)