import sys

file = open(sys.argv[1], "r+")

output = open("generic_colors.txt", "w+")
white = ["white", "snow", "linen", "tan", "khaki", "beige", "silver", "blanchedalmond","ivory","oldlace"]
brown = ["brown", "maroon", "sienna", "peru", "wood", "chocolate"]
yellow = ["gold", "wheat", "yellow", "tan","moccasin","bisque","lemon","corn"]
green = ["green", "teal", "olive", "turquoise", "sea", "mint", "aqua", "coral","lime","honeydew"]
orange = ["orange"]
red = ["red", "rose", "salmon", "fire", "rosy", "crimson","pink","peach","tomato"]
purple = ["lavender", "violet", "purple", "plum", "orchid","thistle","azure","magenta"]
blue = ["blue", "cyan", "navy", "indigo"]
grey = ["grey", "gainsboro"]
for line in file:
    line = line.replace("\n","")
    # print(line)
    for x in white:
        if (x) in line:
            line = "white"
    for x in brown:
        if (x) in line:
            line = "brown"
    for x in yellow:
        if (x) in line:
            line = "yellow"
    for x in green:
        if (x) in line:
            line = "green"
    for x in orange:
        if (x) in line:
            line = "orange"
    for x in red:
        if (x) in line:
            line = "red"
    for x in purple:
        if (x) in line:
            line = "purple"
    for x in blue:
        if (x) in line:
            line = "blue"
        # print(line)
    for x in grey:
        if (x) in line:
            line = "grey"
        # print(line)
    # sleep(1)
    line = line + "\n"
    output.write(line)