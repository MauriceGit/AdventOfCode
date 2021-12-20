#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *




def get_bin(img, x, y, default="0"):

    n =  default if (x-1,y-1) not in img else img[(x-1,y-1)]
    n += default if (x,  y-1) not in img else img[(x,y-1)]
    n += default if (x+1,y-1) not in img else img[(x+1,y-1)]
    n += default if (x-1,y  ) not in img else img[(x-1,y)]
    n += default if (x,  y  ) not in img else img[(x,y)]
    n += default if (x+1,y  ) not in img else img[(x+1,y)]
    n += default if (x-1,y+1) not in img else img[(x-1,y+1)]
    n += default if (x,  y+1) not in img else img[(x,y+1)]
    n += default if (x+1,y+1) not in img else img[(x+1,y+1)]

    return n


def apply_algorithm(img, algorithm, n=0):

    output_image = defaultdict(lambda: "0")

    extend = 2 if n==0 else 5
    minx = min(img.keys(), key=lambda x:x[0])[0]-extend
    maxx = max(img.keys(), key=lambda x:x[0])[0]+extend
    miny = min(img.keys(), key=lambda x:x[1])[1]-extend
    maxy = max(img.keys(), key=lambda x:x[1])[1]+extend

    for y in range(miny, maxy):
        for x in range(minx, maxx):
            n = get_bin(img, x, y, "0" if n == 0 else "1")
            n = int(n, 2)
            output_image[(x,y)] = algorithm[n]

    return output_image




def main():

    groups = open_data_groups("20.data")

    algorithm = groups[0][0].replace(".", "0").replace("#", "1")

    lines = groups[1]

    image = defaultdict(lambda: "0")
    for y,l in enumerate(lines):
        for x,c in enumerate(l):
            image[(x,y)] = "0" if c == "." else "1"

    for i in range(2):
        image = apply_algorithm(image, algorithm)

    print(len(lfilter(lambda x: x == "1", image.values())))


    # ? 5985 with extend == 2
    # ? 5538 with extend == 1

if __name__ == "__main__":
    main()

# year 2021
# solution for 20.01: ?
# solution for 20.02: ?
