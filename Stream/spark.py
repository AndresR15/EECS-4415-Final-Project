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
import re
import csv

#IP of user outside of docker
IP = '192.168.0.14'
time = ""
amoun = 0

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

def sentiment(line):
    #print(line)
    r1 = re.search('\?v=([^&]+)&*', line)
    r2 = re.search('youtu.be\/([^?]+)\?*', line)
    #re.search('\?v=([^&]+)&*', request.url)
    time = datetime.datetime.now()
    time = time - datetime.timedelta(minutes=time.minute % 1,seconds=time.second,microseconds=time.microsecond)
    time = time.strftime("%Y-%m-%d-%H-%M-%S")
    if r1:
        return str(time) + " " + r1.group(1) 
    elif r2:
        return str(time) + " " + r2.group(1) 
    else:
        return "none"

links = dataStream.map(sentiment)
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
    videos = {}
    times = []

    print("----------- %s -----------" % str(time))
    try:
        # sort counts (desc) in this time instance and take top 10
        sorted_rdd = rdd.sortBy(lambda x:x[0], False)
        top10 = sorted_rdd.collect()
        # print it nicely
        

        for tag in top10:
            print('{:<40} {}'.format(tag[0], tag[1]))
            print(time)
            print(amoun)
            if not tag[0].split(" ")[0] in times:
                for key in videos:
                    while len(videos[key]) < amoun:
                        videos[key].append(0)
                amoun += 1
                time = tag[0].split(" ")[0]
                times.append(time)
            if tag[0].split(" ")[1] in videos:
                videos[tag[0].split(" ")[1]].append(tag[1])
            else:
                videos[tag[0].split(" ")[1]] = [tag[1]]
            
        
        send_df_to_dashboard(times,videos)
        
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e)


def send_df_to_dashboard(video, count):
    # set up url with user's ip
    url = 'http://'+ IP + ':5001/updateData'
    print(video)
    print(count)
    # initialize and send the data through REST API
    request_data = {'labels': str(video), 'data': str(count)}

    response = requests.post(url, data=request_data) 

# do this for every single interval
words_totals.foreachRDD(process_interval)


# start the streaming computation
ssc.start()
# wait for the streaming to finish
ssc.awaitTermination()