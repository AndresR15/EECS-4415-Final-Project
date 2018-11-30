#!/usr/bin/env python

# built from the tutorial template 
# data visualization implementation copied from
# https://www.toptal.com/apache/apache-spark-streaming-twitter

import sys, requests, socket
import pyspark as ps
from pyspark import SparkConf,SparkContext
import pyspark.streaming as pss
from pyspark.sql import Row,SQLContext

IP = "192.168.0.20"

def main(hashtags):
	global IP

	# start connection
	# configure spark instance to default
	config = SparkConf()
	config.setAppName("Twitter_Stream_Analasys")
	s_context = SparkContext(conf = config)
	# To prevent drowing the terminal, only log error messages?
	s_context.setLogLevel("ERROR")

	# use spark context to create the stream context
	# interval size = 2 seconds
	s_stream_context = pss.StreamingContext(s_context, 2)
	s_stream_context.checkpoint("checkpoint_TSA")

	# connect to port 9009 (the one used by twitter_trends)
	socket_ts = s_stream_context.socketTextStream("twitter", 9009)

	print("Clear setup\n\n\n\n\n\n\n")

	# retreve streamed text, split input into array of words
	
	#tweet_text = socket_ts

	# remove all words that arent emotions'
	words = socket_ts.flatMap(lambda line: line.split(" "))

	i_hashtags = words.filter(check_topic)
	
	# map each hashtag (map reduce to count)
	hashtag_count = i_hashtags.map(lambda x: (x.lower(), 1))	

	# do the aggregation, note that now this is a sequence of RDDs
	hashtag_totals = hashtag_count.updateStateByKey(aggregate_tags_count)

	# do this for every single interval
	hashtag_totals.foreachRDD(process_interval)

	#set up sql 
	sql_context = get_sql_context_instance(s_context)

	# start the streaming computation
	s_stream_context.start()

	try:
		# wait for the streaming to finish
		s_stream_context.awaitTermination()
	except KeyboardInterrupt:
		print("\nSpark shutting down\n")

# process a single time interval
def process_interval(time, rdd):
	# print a separator
	print("----------- %s -----------" % str(time))
	try:
		for tag in rdd.collect():
			# Get spark sql singleton context from the current context
			sql_context = get_sql_context_instance(rdd.context)

			# convert the RDD to Row RDD
			row_rdd = rdd.map(lambda w: Row(hashtag=w[0], hashtag_count=w[1]))

			# create a DF from the Row RDD
			hashtags_df = sql_context.createDataFrame(row_rdd)
			# Register the dataframe as table
			hashtags_df.registerTempTable("hashtags")
			# print out all hashtags with teir counts 

			hashtag_counts_df = sql_context.sql("select hashtag, hashtag_count from hashtags")
			hashtag_counts_df.show()
			# call this method to prepare top 10 hashtags DF and send them
			send_df_to_dashboard(hashtag_counts_df)

	except:
		e = sys.exc_info()[0]
		print("Error: {}".format(e))


# adding the count of each hashtag to its last count
# from tutorial code
def aggregate_tags_count(new_values, total_sum):
	return sum(new_values) + (total_sum or 0)	

def arg_error_check():
	global hashtags
	# when no arguments are passed, use default emotions
	if (len(sys.argv) < 2):
		hashtags = ['https://www.youtube.com/watch?v=HKbtt_Xmcqo', 'http://youtu.be/HKbtt_Xmcqo?a']

	# otherwise, add the hashtags into the list
	else:
		#since the first element of sys.argv is the python script name, lets skip it and iterate through the rest
		input_hashtags = sys.argv

		for tag in input_hashtags[1:]:
			try:
				hashtags.append(str(tag))
			except ValueError:
				# if for some reason the input could not be converted to a string
				raise ValueError("{} could not be converted to string".format(tag))
		
	#connect with twitter and filter out using the hashtags provided
	main(hashtags)

def check_topic(text):
	for word in text.split(" "):
		if word.lower() in hashtags:
			return True
	return False

def get_sql_context_instance(spark_context):
	if ('sqlContextSingletonInstance' not in globals()):
		globals()['sqlContextSingletonInstance'] = SQLContext(spark_context)
	return globals()['sqlContextSingletonInstance']    

def send_df_to_dashboard(df):
	# extract the hashtags from dataframe and convert them into array
	tags = [str(t.hashtag) for t in df.select("hashtag").collect()]

	# extract the counts from dataframe and convert them into array
	tags_count = [p.hashtag_count for p in df.select("hashtag_count").collect()]

	# set up url with user's ip
	url = 'http://'+ IP + ':5002/updateData'

	# initialize and send the data through REST API
	request_data = {'label': str(tags), 'data': str(tags_count)}

	response = requests.post(url, data=request_data) 


if __name__ == "__main__": arg_error_check()	



