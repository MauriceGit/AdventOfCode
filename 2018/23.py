#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def dist(b1, b2):
    s = sub3(b1[0], b2[0])
    return abs(s[0])+abs(s[1])+abs(s[2])

def main():

    lines = open_data("23.data")

    nanobots = []
    for l in lines:
        x,y,z,r = ints(l)
        nanobots.append(((x,y,z), r))

    best_bot = max(nanobots, key=lambda x: x[1])

    print(sum(dist(b, best_bot) <= best_bot[1] for b in nanobots))




if __name__ == "__main__":
    main()

# year 2018
# solution for 23.01: ?
# solution for 23.02: ?
