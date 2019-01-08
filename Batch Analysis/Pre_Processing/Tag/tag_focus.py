# Prepossesses cvs file that is inputed
# Expected schema:   |artist name|song name|link|lyrics|
#
import sys, csv, re, math
from itertools import combinations

def clean_input(input):
	# this function will clean the input by removing unnecessary punctuation
	
	# input must be of type string
	if type(input) != str:
		raise TypeError("input not a string type")
	
	# first any contractions are collapsed by removing the apostrophes
	temp = re.sub(r'[\']', '', input)

	# next, remove quotes
	temp.replace('"', '')

	# next, the input must be stripped of punctuation
	# this is done by replacing them with whitespace 
	temp = re.sub(r'[^\w\s\|]', '' , temp)

	#remove all newlines 
	temp = re.sub(r'[\n]', '', temp)

	return temp

def tag_combination(tag):
	print('______' + tag + '______')
	# returns every possible conbination of every word inside the tag
	tag_combinations = []
	s_tag = tag.split()
	if len(s_tag) > 1:
		for x in range(1, len(s_tag)):
			for tag_set in combinations(s_tag, x):
				tag_combinations.append(tag_set)

		print('\t' + str(tag_combinations))
	else:
		tag_combinations.append(tag)

	return tag_combinations

def main():
		# open csv file
	reader = csv.reader(sys.stdin)
	next(reader) # skip header

	#create txt file
	file = open("tag_data.txt", "w+")

	# for each row in the csv, write each songs lyrics to the txt file
	count = 0
	for row in reader:

		total_tag_combos = []
		#get tags from csv file and "clean" them
		tags = clean_input(row[6]).split("|")

		if len(tags) == 0:
			continue

		#get all combinations for a tag
		for tag in tags:
			total_tag_combos.extend(tag_combination(tag))

		file.write(",".join(total_tag_combos))

if __name__ == "__main__": main()







