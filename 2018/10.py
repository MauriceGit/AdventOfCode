#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def main():

    lines = open_data("10.data")

    stars = lmap(lambda x: [[x[0],x[1]], [x[2],x[3]]], map(ints, lines))

    l = [x[0][0] for x in stars]
    x_dist = max(l) - min(l)
    count = 0

    while True:

        for i,s in enumerate(stars):
            stars[i][0] = add(stars[i][0], s[1])

        l = [x[0][0] for x in stars]
        d = max(l) - min(l)
        count += 1

        if d > x_dist:
            for i,s in enumerate(stars):
                stars[i][0] = add(stars[i][0], mul(s[1],-1))

            draw({s[0]: 0 for s in stars}, symbols={-1: ".", 0: "█", 1: "#"})
            print(count-1)
            break
        x_dist = d


if __name__ == "__main__":
    main()

# year 2018
# solution for 10.01: KFLBHXGK
# solution for 10.02: 10659
