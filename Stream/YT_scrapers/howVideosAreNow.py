from backports import csv
import io
import re

averageViewChange = 0
averageLikeChange = 0
averageDislikeChange = 0
biggestViewJump = 0
idOfBiggestViewJump = ""
smallestViewJump = 0
idOfSmallestViewJump = ""
top5Views = [0,0,0,0,0]
bottom5Views = [100000000,100000000,100000000,100000000,100000000]
with io.open("newCSV.csv", newline='', encoding='ISO-8859-1') as videos:
    csvReader = csv.reader(videos)
    next(csvReader,None)
    for row in csvReader:
        if re.search(r"\d+", row[3]):
            averageViewChange = (averageViewChange + (int(row[3]) - int(row[9]))) / 2

            top5Views.append((int(row[3]) - int(row[9])))
            smallest = top5Views[0]
            for i in top5Views:
                if i < smallest:
                    smallest = i
            top5Views.remove(smallest); 
            if (int(row[3]) - int(row[9])) > 0:
                bottom5Views.append((int(row[3]) - int(row[9])))
                largest = bottom5Views[0]
                for i in bottom5Views:
                    if i > largest:
                        largest = i
                bottom5Views.remove(largest); 

            if (int(row[3]) - int(row[9])) > biggestViewJump:
                idOfBiggestViewJump = row[0]
                biggestViewJump = (int(row[3]) - int(row[9]))
            if (int(row[3]) - int(row[9])) < smallestViewJump:
                idOfSmallestViewJump = row[0]
                smallestViewJump = (int(row[3]) - int(row[9]))
        if re.search(r"\d+", row[6]):
            averageLikeChange = (averageLikeChange + (int(row[6]) - int(row[10]))) / 2
        if re.search(r"\d+", row[5]):
            averageDislikeChange = (averageDislikeChange + (int(row[5]) - int(row[11]))) / 2

    print("average view change: " +  str(averageViewChange))
    print("average like change: " +  str(averageLikeChange))
    print("average dislike change: " +  str(averageDislikeChange))
    print("biggest view change: " + str(biggestViewJump))
    print("id of biggest view change: " + idOfBiggestViewJump)
    print("smallest view change: " + str(smallestViewJump))
    print("id of smallest view change: " + idOfSmallestViewJump)
    print("top 5 views changes were: " + str(top5Views))
    print("bottom 5 view changes were: " + str(bottom5Views))