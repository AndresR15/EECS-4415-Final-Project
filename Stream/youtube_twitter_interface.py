#!/usr/bin/env python

import sched, time, requests
import twitter_trends as twitter_stream

def main():
	#set up scheduler 
	global s
	s = sched.scheduler(time.time, time.sleep)
	s.enter(1, 1, twitter_listner)

	s.run()

def scrape_data():
	# ping youtube
	request_url = "https://www.googleapis.com/youtube/v3/videos?part=id,statistics,snippet&maxResults=50&key=AIzaSyDqgKq1M-UHx_3rYmOmUGP-guN5iwW6SEE&chart=mostPopular&regionCode=CA"
	request = requests.get(request_url)
	# split responce into json 
	json = request.json()

	ids = []
	# if theres no error, get the video id for each trending video
	if "items" in json:
		for item in json["items"]:
			if item:
				ids.append(item["id"])
				# line.append(item["snippet"]["title"])
				# line.append(item["snippet"]["categoryId"])
				# line.append(item["snippet"]["publishedAt"])	
	#print(str(ids))

	return ids

def twitter_listner(): 
	# run scraper 
	scraped_urls = scrape_data() 

	print ("Restarting twitter stream")
	# run twitter stream with urls
	twitter_stream.connect_twitter(scraped_urls)
	
	# do your stuff
	s.enter(900, 1, twitter_listner)


if __name__ == "__main__": main()	



