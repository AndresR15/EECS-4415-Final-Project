import struct
from PIL import Image
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
import sys
import requests
import webcolors
import codecs
import cv2
import time

file = open(sys.argv[1], "r+", errors='ignore')

NUM_CLUSTERS = 5
next(file)

def classify_common_color(im):
    ar = np.asarray(im)
    shape = ar.shape
    ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

    # print('finding clusters')
    codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
    # print('cluster centres:\n', codes)

    vecs, dist = scipy.cluster.vq.vq(ar, codes)  # assign codes
    counts, bins = scipy.histogram(vecs, len(codes))  # count occurrences
    index_max = scipy.argmax(counts)  # find most frequent
    peak = codes[index_max]
    # print(peak)
    new_peak = (int(peak[0]), int(peak[1]), int(peak[2]))
    # print(new_peak)
    closest_name = get_colour_name(new_peak)
    return closest_name

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
    return closest_name

output = open("output.txt", "w+")
for i, line in enumerate(file):
    try:
        imageurl = line.split(",")[1]
        # print("|" + imageurl + "|")
        imageurl = imageurl.replace("\n","")
        # print("|" + imageurl + "|")
        response = requests.get(imageurl, stream=True)
        # print("-----------------------------------------------------------")
        # print(response.content)

        open("image.jpg", 'wb').write(response.content)
        # print(response)
        im = Image.open("image.jpg")
        # print(type(im))
        im = cv2.imread("image.jpg")
        # print("Here")
        cropped = im[20:70, :]
        # print("Here1")
        color = classify_common_color(cropped)
        # print("Here3")
        # print(color)
        # print(color == "lightgrey")
        if color == "lightgrey":
            # string = str(i + 1) + ", " + "Default" + "\n"
            string = "Default" + "\n"
            output.write(string)
        else:
            string = color + "\n"
            output.write(string)
    except:
        string = "Failed" + "\n"
        output.write(string)



