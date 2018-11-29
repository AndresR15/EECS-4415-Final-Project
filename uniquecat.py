import requests
import csv
import io

category = 4
categories = []

with io.open("CAvideos.csv", newline='', encoding='utf-8') as videos:
	csvReader = csv.reader(videos)
	next(csvReader,None)
	for row in csvReader:
		var = row[category]
		if var not in categories and var is not "category_id":
			categories.append(var)
categories.sort()
print(categories)