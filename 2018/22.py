#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *

@lru_cache(maxsize=1000000)
def calc_geo_index(pos, target, depth):
    if pos == (0,0):
        return 0
    if pos == target:
        return 0
    if pos[1] == 0:
        return pos[0]*16807
    if pos[0] == 0:
        return pos[1]*48271
    return calc_erosion_level(add(pos,(-1,0)), target, depth) * calc_erosion_level(add(pos,(0,-1)), target, depth)


@lru_cache(maxsize=1000000)
def calc_erosion_level(pos, target, depth):
    return (calc_geo_index(pos, target, depth) + depth) % 20183


def main():

    lines = open_data("22.data")
    depth = ints(lines[0])[0]
    target = tuple(ints(lines[1]))

    #depth = 510
    #target = (10,10)

    risk_level = 0
    for y in range(target[1]+1):
        for x in range(target[0]+1):
            risk_level += calc_erosion_level((x,y), target, depth) % 3


    print(risk_level)




if __name__ == "__main__":
    main()

# year 2018
# solution for 22.01: ?
# solution for 22.02: ?
