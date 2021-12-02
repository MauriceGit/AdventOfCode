#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def part1(t):
    v = int(t[1])
    return {"forward": (v,0), "down": (0, v), "up": (0, -v)}[t[0]]

def part2(t):
    v = int(t[1])
    return {"forward": (int(t[1]),0), "down": (0, int(t[1])), "up": (0, -int(t[1]))}[t[0]]

def main():

    lines = open_data("02.data")

    p = reduce(add, [part1(l.split(" ")) for l in lines])
    print(p[0]*p[1])




    p = (0,0,0)
    for l in lines:
        v = ints(l)[0]
        if l.startswith("forward"):
            p = add(p, (v,v*p[2],0))
        if l.startswith("down"):
            p = add(p, (0,0,v))
        if l.startswith("up"):
            p = add(p, (0,0,-v))

    print(p[0]*p[1])




if __name__ == "__main__":
    main()

# year 2021
# solution for 02.01: ?
# solution for 02.02: ?
