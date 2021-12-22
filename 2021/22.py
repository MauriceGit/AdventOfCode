#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *

Cube = recordtype("Cube", "x0 x1 y0 y1 z0 z1")

def no_overlap(c0, c1):
    c1 = c0.x1 < c1.x0 or c1.x1 < c0.x0
    c2 = c0.y1 < c1.y0 or c1.y1 < c0.y0
    c3 = c0.z1 < c1.z0 or c1.z1 < c0.z0
    return c1 or c2 or c3

def diff_cube(c0, c1, f):
    return Cube(f(c0.x0, c1.x0), f(c0.x1, c1.x1), f(c0.y0, c1.y0), f(c0.y1, c1.y1), f(c0.z0, c1.z0), f(c0.z1, c1.z1))

def overlap_region(c0, c1):
    return Cube(max(c0.x0, c1.x0), min(c0.x1, c1.x1), max(c0.y0, c1.y0), min(c0.y1, c1.y1), max(c0.z0, c1.z0), min(c0.z1, c1.z1))

def other_overlaps(c0, c1):
    return [
        Cube(min(c0.x0, c1.x0), max(c0.x0, c1.x0), max(c0.y0, c1.y0), min(c0.y1, c1.y1), max(c0.z0, c1.z0), min(c0.z1, c1.z1)),
        Cube(min(c0.x1, c1.x1), max(c0.x1, c1.x1), max(c0.y0, c1.y0), min(c0.y1, c1.y1), max(c0.z0, c1.z0), min(c0.z1, c1.z1)),

        Cube(max(c0.x0, c1.x0), min(c0.x1, c1.x1), min(c0.y0, c1.y0), max(c0.y0, c1.y0), max(c0.z0, c1.z0), min(c0.z1, c1.z1)),
        Cube(max(c0.x0, c1.x0), min(c0.x1, c1.x1), min(c0.y1, c1.y1), max(c0.y1, c1.y1), max(c0.z0, c1.z0), min(c0.z1, c1.z1)),

        Cube(max(c0.x0, c1.x0), min(c0.x1, c1.x1), max(c0.y0, c1.y0), min(c0.y1, c1.y1), min(c0.z0, c1.z0), max(c0.z0, c1.z0)),
        Cube(max(c0.x0, c1.x0), min(c0.x1, c1.x1), max(c0.y0, c1.y0), min(c0.y1, c1.y1), min(c0.z1, c1.z1), max(c0.z1, c1.z1)),



        Cube(min(c0.x0, c1.x0), max(c0.x1, c1.x1), min(c0.y0, c1.y0), max(c0.y1, c1.y1), max(c0.z0, c1.z0), min(c0.z1, c1.z1)),
        Cube(min(c0.x0, c1.x0), max(c0.x1, c1.x1), max(c0.y0, c1.y0), min(c0.y1, c1.y1), min(c0.z0, c1.z0), max(c0.z1, c1.z1)),

        Cube(max(c0.x0, c1.x0), min(c0.x1, c1.x1), min(c0.y0, c1.y0), max(c0.y0, c1.y0), min(c0.z0, c1.z0), max(c0.z1, c1.z1)),
        Cube(min(c0.x0, c1.x0), max(c0.x1, c1.x1), min(c0.y0, c1.y0), max(c0.y0, c1.y0), max(c0.z0, c1.z0), min(c0.z1, c1.z1)),

        Cube(min(c0.x0, c1.x0), max(c0.x1, c1.x1), max(c0.y0, c1.y0), min(c0.y1, c1.y1), min(c0.z0, c1.z0), max(c0.z1, c1.z1)),
        Cube(max(c0.x0, c1.x0), min(c0.x1, c1.x1), min(c0.y0, c1.y0), max(c0.y1, c1.y1), min(c0.z0, c1.z0), max(c0.z1, c1.z1))
    ]

def overlaps(c0, c1):
    new_cubes = []

    cc0 = diff_cube(c0, c1, min)
    cc1 = diff_cube(c0, c1, max)
    overlapping = overlap_region(c0, c1)
    other = other_overlaps(c0, c1)

    return []


def main():

    lines = open_data("22.data")


    grid = defaultdict(int)
    for l in lines:
        x0,x1,y0,y1,z0,z1 = ints(l)
        on = l.startswith("on")
        if min(x0,y0,z0) >= -50 and max(x1,y1,z1) <= 50:
            for x in range(x0,x1+1):
                for y in range(y0,y1+1):
                    for z in range(z0,z1+1):
                        grid[(x,y,z)] = int(on)

    print(len(lfilter(lambda x: x==1, grid.values())))


    cubes = []
    for l in lines:
        x0,x1,y0,y1,z0,z1 = ints(l)
        on = l.startswith("on")
        cube = Cube(x0,x1,y0,y1,z0,z1)
        for c in cubes:
            if not no_overlap(c, cube):









if __name__ == "__main__":
    main()

# year 2021
# solution for 22.01: ?
# solution for 22.02: ?
