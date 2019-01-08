# tag mapper

import sys

def main():
	#iterate through csv file, reading each line through standard input
	for i_input in sys.stdin:
		tags = i_input.split(",")
		for tag in tags: 
			print("{}\t1".format(tag))

if __name__ == "__main__": main()		