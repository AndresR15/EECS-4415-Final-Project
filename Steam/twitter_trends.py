#!/usr/bin/env python 
import sys, json, socket

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Stream

# Constants (Twitter API access)
ACCESS_TOKEN ="1062409428710973440-nfSRK68aDH1SF0KzD8k3qNhh2BZVk3"
ACCESS_TOKEN_SECRET ="M2WkexSpQvP7mFiYZsd7AR1qUXKiNCZS5MAxetQuqEDDe"
CONSUMER_KEY ="op0ObDPn4TkrkMK6ThmdI5eW2"
CONSUMER_SECRET ="bPXLxN3EX04RAVrmnI7P2fTAjXbHbyiK2mynwOUfZ3BbRuei1r"

# This is a basic listener that just prints received tweets to stdout.
# Taken from http://adilmoujahid.com/posts/2014/07/twitter-analytics/
class tweet_listner(StreamListener):

	def on_data(self, data):
		try:
			

			# load the tweet JSON, get pure text
			full_tweet = json.loads(data)
			tweet_text = full_tweet['text']

			# print the tweet plus a separator
			print ("------------------------------------------")
			print (tweet_text + '\n')

			# send it to spark
			conn.send(str.encode(tweet_text + '\n'))
		except:
			# print error
			e = sys.exc_info()[0]
			print("Error: %s" % e)
		return True

	def on_error(self, status):
		# if an error is encountered, print it to stdout
		print(status)


def connect_twitter(youtube_link):
	# set up connection to local machine
	global conn
	#get local port
	LOCAL_IP = socket.gethostbyname(socket.gethostname()) 
	PORT = 9009

	# start up local connection (from tutorial slides)
	conn = None
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((LOCAL_IP, PORT))
	s.listen(1)
	print("Waiting for TCP connection...")

	# if the connection is accepted, proceed
	conn, addr = s.accept()
	print("Connected... Starting getting tweets.")


	# uses twitter API key to connect and start stream with the provided keys
	listener = tweet_listner()
	auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	stream = Stream(auth, listener)

	#language = ['en']
	try:
		# only shows tweets containing the specified hashtags 
		stream.filter(track=youtube_link)
	except KeyboardInterrupt:
		s.shutdown(socket.SHUT_RD)

if __name__ == "__main__": 
	test_url = ["www.youtube.com/watch?v=wXlBep9uFjI", 'http://youtu.be/wXlBep9uFjI?a', "youtu.be/wXlBep9uFjI"]
	connect_twitter(test_url)	

