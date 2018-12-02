"""
    This Spark app connects to a script running on another (Docker) machine
    on port 9009 that provides a stream of raw tweets text. That stream is
    meant to be read and processed here, where top trending hashtags are
    identified. Both apps are designed to be run in Docker containers.

    To execute this in a Docker container, do:
    
        docker run -it -v $PWD:/app --link twitter:twitter eecsyorku/eecs4415

    and inside the docker:

        spark-submit spark_app.py

    For more instructions on how to run, refer to final tutorial 8 slides.

    Made for: EECS 4415 - Big Data Systems (York University EECS dept.)
    Modified by: Tilemachos Pechlivanoglou
    Based on: https://www.toptal.com/apache/apache-spark-streaming-twitter
    Original author: Hanee' Medhat

"""

from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row,SQLContext
import sys
import requests, datetime
from textblob import TextBlob
import re
import csv


# create spark configuration
conf = SparkConf()
conf.setAppName("TwitterStreamApp")
# create spark context with the above configuration
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")
# create the Streaming Context from spark context, interval size 2 seconds
ssc = StreamingContext(sc, 2)
# setting a checkpoint for RDD recovery (necessary for updateStateByKey)
ssc.checkpoint("checkpoint_TwitterApp")
# read data from port 9009
dataStream = ssc.socketTextStream("twitter",9009)

# reminder - lambda functions are just anonymous functions in one line:
#
#   words.flatMap(lambda line: line.split(" "))
#
# is exactly equivalent to
#
#    def space_split(line):
#        return line.split(" ")
#
#    words.filter(space_split)

# split each tweet into words
#words = dataStream.Map(lambda line: line.split()
# filter the words to get only hashtags
#category = words.filter()
#hashtags = words.filter(lambda w: '#' in w)

def ping_url(line):
    #print(line)
    r1 = re.search('\?v=([^&]+)&*', line)
    r2 = re.search('youtu.be\/([^?]+)\?*', line)
    #re.search('\?v=([^&]+)&*', request.url)
    #time = (datetime.datetime.now() + datetime.timedelta(minutes=15) % datetime.timedelta(minutes=15))
    if r1:
        return r1.group(1)
    elif r2:
        return r2.group(1)
    else:
        return "none"
links = dataStream.map(ping_url)
words = links.map(lambda x: (x, 1))
words = words.filter(lambda w: 'none' not in w)
# map each hashtag to be a pair of (hashtag,1)
#hashtag_counts = hashtags.map(lambda x: (x, 1))

# adding the count of each hashtag to its last count

def sentiment_analysis(new_values, total_sum):
    return sum(new_values) + (total_sum or 0)

words_totals = words.updateStateByKey(sentiment_analysis)

# do the aggregation, note that now this is a sequence of RDDs
#hashtag_totals = hashtag_counts.updateStateByKey(aggregate_tags_count)

# process a single time interval
def process_interval(time, rdd):
    # print a separator
    cate = []
    values = []
    print("----------- %s -----------" % str(time))
    try:
        # sort counts (desc) in this time instance and take top 10
        sorted_rdd = rdd.sortBy(lambda x:x[1], False)
        top10 = sorted_rdd.collect()
        # print it nicely
        for tag in top10:
            print('{:<40} {}'.format(tag[0], tag[1]))
            #csvWriter.writerow([tag[0], tag[1]])
        
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e)


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

# do this for every single interval
words_totals.foreachRDD(process_interval)


# start the streaming computation
ssc.start()
# wait for the streaming to finish
ssc.awaitTermination()