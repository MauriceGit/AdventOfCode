#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def apply_algorithm(img, algorithm, roundzero=True):

    output_image = defaultdict(lambda: "1" if roundzero else "0")

    minx = min(img.keys(), key=lambda x:x[0])[0]-1
    maxx = max(img.keys(), key=lambda x:x[0])[0]+1+1
    miny = min(img.keys(), key=lambda x:x[1])[1]-1
    maxy = max(img.keys(), key=lambda x:x[1])[1]+1+1

    for y in range(miny, maxy):
        for x in range(minx, maxx):
            n = int(img[(x-1,y-1)]+img[(x,y-1)]+img[(x+1,y-1)]+img[(x-1,y)]+img[(x,y)]+img[(x+1,y)]+img[(x-1,y+1)]+img[(x,y+1)]+img[(x+1,y+1)], 2)
            output_image[(x,y)] = algorithm[n]

    return output_image


def main():

    groups = open_data_groups("20.data")

    algorithm = groups[0][0].replace(".", "0").replace("#", "1")

    image = defaultdict(lambda: "0")
    for y,l in enumerate(groups[1]):
        for x,c in enumerate(l):
            image[(x,y)] = "0" if c == "." else "1"

    for i in range(50):
        image = apply_algorithm(image, algorithm, roundzero=i%2==0)
        if i == 1:
            print(sum(map(int, image.values())))
    print(sum(map(int, image.values())))


if __name__ == "__main__":
    main()

# year 2021
# solution for 20.01: 5647
# solution for 20.02: 15653
