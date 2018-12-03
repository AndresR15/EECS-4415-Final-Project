import requests
import csv
import io
import sys

id = 3
title = 1
category = 0
desc = 2
ccat = '-1'
sum = 0.0
titlesentp = [0.0,0.0,0.0,0.0]
descsentp = [0.0,0.0,0.0,0.0]
titlesent = [0,0,0]
descsent = [0,0,0]
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
			sum = descsent[0] + descsent[1] + descsent[2];
			descsentp[0] = descsent[0] / sum;
			descsentp[1] = descsent[1] / sum;
			descsentp[2] = descsent[2] / sum;
			descsentp[3] = (descsent[0] - descsent[2]) / sum;
			sum = titlesent[0] + titlesent[1] + titlesent[2];
			titlesentp[0] = titlesent[0] / sum;
			titlesentp[1] = titlesent[1] / sum;
			titlesentp[2] = titlesent[2] / sum;
			titlesentp[3] = (titlesent[0] - titlesent[2]) / sum;
			print(ccat + ":" + str(titlesentp) + ":" + str(descsentp))
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

# output string is catagory name, title sentiments, then description sentiments
sum = descsent[0] + descsent[1] + descsent[2];
descsentp[0] = descsent[0] / sum;
descsentp[1] = descsent[1] / sum;
descsentp[2] = descsent[2] / sum;
descsentp[3] = (descsent[0] - descsent[2]) / sum;
sum = titlesent[0] + titlesent[1] + titlesent[2];
titlesentp[0] = titlesent[0] / sum;
titlesentp[1] = titlesent[1] / sum;
titlesentp[2] = titlesent[2] / sum;
titlesentp[3] = (titlesent[0] - titlesent[2]) / sum;
print(ccat + ":" + str(titlesentp) + ":" + str(descsentp))