import csv
import tweepy
from pprint import pprint
from tweepy import OAuthHandler

consumer_key="nUyozpqmr0aXnCEFRVGjrPYAb"
consumer_secret="b51eVIcS7yiCWfs8btEK0yfNcbU4C0qqIGsfPI2FKcPsWQwRcr"
access_token="1061977244971790336-6gGipYDM0US92WNzM7hAovsyeSQ5cW"
access_token_secret="Slgj6N99rprjaKCrN38lErvYbkbWiHoYak8k6Qp7q2yLY"

# ==== setup twitter connection ====
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


csvFile = open('tweets.csv', 'a')
csvWriter = csv.writer(csvFile)
api = tweepy.API(auth)


for tweet in api.search(q="#PS4",count=100,lang="en",since_id=2018-11-27):
    print(tweet.created_at, tweet.text)
    csvWriter.writerow([tweet.created_at, tweet.text])