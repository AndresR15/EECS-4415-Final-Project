import sys
import webcolors
# Open file from command line
file = open(sys.argv[1], "r+")

output = open("output.txt", "w+")


for line in file:
    try:
        temp = line.replace("\n","")
        color = webcolors.name_to_rgb(temp)
        string = str(color) + "\n"
        # print(string)
        output.write(string)
    except:
        string = "Failed" + "\n"
        # print(string)
        output.write(string)
