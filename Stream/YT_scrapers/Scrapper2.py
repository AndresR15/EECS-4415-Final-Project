import requests
import csv
import io
import datetime

def main();
    data = ["VideoId", "title", "commentCount", "viewCount", "favoriteCount", "dislikeCount", "likeCount", "channel", "tags", "description", "categoryId", "Publish date", "time"]
        
    #for row in csvReader:

    request_url = "https://www.googleapis.com/youtube/v3/videos?part=id,statistics,snippet&maxResults=50&key=AIzaSyDqgKq1M-UHx_3rYmOmUGP-guN5iwW6SEE&chart=mostPopular&regionCode=CA"
    request = requests.get(request_url)
    json = request.json()
    #print(json)

    with io.open("scrapped.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(data)
        if "items" in json:
            for item in json["items"]:
                line = []
                if item:
                    line.append(item["id"])
                    line.append(item["snippet"]["title"])
                    line.append(item["statistics"]["commentCount"])
                    line.append(item["statistics"]["viewCount"])
                    line.append(item["statistics"]["favoriteCount"])
                    line.append(item["statistics"]["dislikeCount"])
                    line.append(item["statistics"]["likeCount"])
                    line.append(item["snippet"]["channelTitle"])
                    tags = []
                    if 'tags' in item["snippet"]:
                        for tag in item["snippet"]["tags"]:
                            tags.append(tag)
                    line.append(tags)
                    line.append(item["snippet"]["description"])
                    line.append(item["snippet"]["categoryId"])
                    line.append(item["snippet"]["publishedAt"])
                    line.append(datetime.datetime.now())
                    writer.writerow(line)

    #for row in data:
    #print row

if __name__ == "__main__": main()   
