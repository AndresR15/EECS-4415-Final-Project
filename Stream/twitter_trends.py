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
			full_tweet = json.loads(data)

			print ("------------------------------------------")
			tweet_text = full_tweet['text']
			tweet_urls = get_urls(full_tweet)
			
			for url in tweet_urls:
				conn.send(str.encode(url + '\n'))
		except:
			# print error
			e = sys.exc_info()[0]
			print("Error: %s" % e)
		return True

	def on_error(self, status):
		# if an error is encountered, print it to stdout
		print(status)

def get_urls(full_tweet):
	# load the tweet JSON, get pure text
	tweet_urls = set()
	#print("\n\n\n\n\n" + str(full_tweet) + "\n\n\n\n\n")
	try:
		for url in full_tweet['entities']['urls']:
			tweet_urls.add(url['expanded_url'])
	except:
		print("not a raw tweet")
	try:
		for url in full_tweet['quoted_status']['entities']['urls']:
			tweet_urls.add(url['expanded_url'])
	except:
		print("not a quoted tweet")
	try:
		for url in full_tweet['extended_tweet']['entities']['urls']:
			tweet_urls.add(url['expanded_url'])
	except:
		print("not an extended tweet")	
	try:
		for url in full_tweet['retweeted_status']['entities']['urls']:
			tweet_urls.add(url['expanded_url'])
	except:
		print("not a retweet")	
	try:
		for url in full_tweet['retweeted_status']['extended_tweet']['entities']['urls']:
			tweet_urls.add(url['expanded_url'])
	except:
		print("not an extended retweet")
				
	print(str(tweet_urls))
	return tweet_urls


def connect_twitter(youtube_links):
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
		stream.filter(track=youtube_links)
	except KeyboardInterrupt:
		s.shutdown(socket.SHUT_RD)

if __name__ == "__main__": 
	test_url = ["gl1aHhXnN1k"]
	connect_twitter(test_url)	

