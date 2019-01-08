#!/usr/bin/env python 

import sys, re

def tag_mapper():
	for line in sys.stdin:
		# before we pass these on to the split function, we must "clean" the input
		song_lyric = clean_input(line.lower())
		lyric_split = song_lyric.split()
		# create a buffer list to hold words that we skipped over
		l_buffer = []

		for word in lyric_split:
			if (len(l_buffer) < buffer_size - 1):
				l_buffer.append(word)
				continue

			elif (len(l_buffer) == buffer_size - 1):
				l_buffer.append(word)

			else:
				l_buffer[buffer_size - 1] = word

			# need to output both n-gram and k-skip-n-gram
			# question specified result = n-gram U k-skip-n-gram
			
			# print out n-gram
			n_string = "" + l_buffer[0]
			for i in range(1, n):
				n_string += " " + l_buffer[i]

			print("{}\t1".format(n_string))

			# print out k-skip-n-gram
			r_sting = "" + l_buffer[0]

			for i in range(1, n):
				r_sting += " " + l_buffer[i * (k + 1)]

			print("{}\t1".format(r_sting))

			# shift all words in the buffer to the left by one
			# word at l_buffer[0] if deleted
			for i in range(1, buffer_size):
				l_buffer[i-1] =l_buffer[i]


def main():
	tag_mapper()


if __name__ == "__main__": main()	