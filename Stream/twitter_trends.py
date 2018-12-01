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
			print (tweet_text)
			
			# print the tweet plus a separator
			if tweet_urls == '':
				#print("\t")
				print (full_tweet)
				#print ("\n\n\n\n\n")
			#	print ('___________|' + tweet_urls + '|___________\n')

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

def get_urls(full_tweet):
	# load the tweet JSON, get pure text
	tweet_urls = ''

	# if someone tweeted the url, it will appear here
	if 'entities' in full_tweet:
			if 'urls' in full_tweet['entities']:
				if len(full_tweet['entities']['urls']) > 0 and 'expanded_url' in full_tweet['entities']['urls'][0]:
					tweet_urls = full_tweet['entities']['urls'][0]['expanded_url']
	# otherwise, if someone just quoted the tweet, we still consider this relevant twitter activity		
	if 'quoted_status' in full_tweet:
		if 'entities' in full_tweet['quoted_status']:
			if 'urls' in full_tweet['quoted_status']['entities']:
				if len(full_tweet['quoted_status']['entities']['urls']) > 0 and 'expanded_url' in full_tweet['quoted_status']['entities']['urls'][0]:
					tweet_urls = full_tweet['quoted_status']['entities']['urls'][0]['expanded_url']
		
		#tweet_urls = full_tweet['quoted_status']['entities']['urls']['expanded_url']
	# also, if someone has access to extended tweeting, we still consider this relevant twitter activity		
	if 'extended_tweet' in full_tweet:
		if 'entities' in full_tweet['extended_tweet']:
			if 'urls' in full_tweet['extended_tweet']['entities']:
				if len(full_tweet['extended_tweet']['entities']['urls']) > 0 and 'expanded_url' in full_tweet['extended_tweet']['entities']['urls'][0]:
					tweet_urls = full_tweet['extended_tweet']['entities']['urls'][0]['expanded_url']
		#tweet_urls = full_tweet['quoted_status']['entities']['urls']['expanded_url']

	# if the tweet was retweeted
	if 'retweeted_status' in full_tweet:
		if 'entities' in full_tweet['retweeted_status']:
			if 'urls' in full_tweet['retweeted_status']['entities']:
				if len(full_tweet['retweeted_status']['entities']['urls']) > 0 and 'expanded_url' in full_tweet['extended_tweet']['entities']['urls'][0]:
					tweet_urls = full_tweet['retweeted_status']['entities']['urls'][0]['expanded_url']
		#tweet_urls = full_tweet['quoted_status']['entities']['urls']['expanded_url']
				

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

