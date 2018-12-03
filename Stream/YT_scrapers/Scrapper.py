import requests
from backports import csv
import io

data = ["VideoId", "title", "commentCount", "viewCount", "favoriteCount", "dislikeCount", "likeCount", "channel", "currentSubCount"]
with io.open("smaller.csv", newline='', encoding='utf-8') as videos:
    csvReader = csv.reader(videos)
    next(csvReader,None)
    
    with io.open("newCSV.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(data)
        for row in csvReader:
            line = []
            request_url = "https://www.googleapis.com/youtube/v3/videos?part=id,statistics,snippet&maxResults=50&key=AIzaSyDqgKq1M-UHx_3rYmOmUGP-guN5iwW6SEE&id=" + row[0]
            request = requests.get(request_url)
            json = request.json()
            #print json
            if json["items"]:
                line.append(json["items"][0]["snippet"]["title"])
                line.append(json["items"][0]["statistics"]["commentCount"])
                line.append(json["items"][0]["statistics"]["viewCount"])
                line.append(json["items"][0]["statistics"]["favoriteCount"])
                line.append(json["items"][0]["statistics"]["dislikeCount"])
                line.append(json["items"][0]["statistics"]["likeCount"])
                writer.writerow(line)


