# tag reducer

import sys

def main():
	last_read = None
	sum = 1

	for line in sys.stdin:
		key, value = line.split('\t')

		if key == last_read:
			sum += 1
		else:
			if last_read != None: 
				print("{}\t{}".format(last_read, sum))
			last_read = key
			sum  = 1
	# now, print the last element that was recived 		
	print("{}\t{}".format(sum, last_read))

if __name__ == "__main__": main()