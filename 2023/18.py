#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *
import shapely


def calc_area(lines, part2=False):
    p = (0,0)
    f = dict()
    boundary_count = 0
    for line in lines:
        d, count, color = line.split(" ")
        count = int(count)
        if part2:
            count = int(color[2:][:-2], 16)
            d = "RDLU"[int(color[-2])]
        boundary_count += count
        p = add(p, mul(direction_map()[d], count))
        f[p] = "#"
    return int(shapely.Polygon(list(f.keys())).area) + boundary_count//2 + 1

def main():

    lines = open_data("18.data")

    print(calc_area(lines))
    print(calc_area(lines, part2=True))


if __name__ == "__main__":
    main()

# year 2023
# solution for 18.01: 67891
# solution for 18.02: 94116351948493
