#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def expand(f, factor):
    f.sort(key=itemgetter(1))
    for i in range(len(f)-1):
        ydiff = f[i+1][1]-f[i][1]
        if ydiff > 1:
            for j in range(i+1, len(f)):
                f[j] = add(f[j], (0, (ydiff-1)*(factor-1)))

    f.sort(key=itemgetter(0))
    for i in range(len(f)-1):
        xdiff = f[i+1][0]-f[i][0]
        if xdiff > 1:
            for j in range(i+1, len(f)):
                f[j] = add(f[j], ((xdiff-1)*(factor-1), 0))
    return f

def main():

    lines = open_data("11.data")

    f = []
    for y,line in enumerate(lines):
        for x,c in enumerate(line):
            if c == "#":
                f.append((x,y))

    ff = expand(f.copy(), 2)
    print(sum(manhatten_dist(g0,g1) for i,g0 in enumerate(ff) for g1 in ff[i+1:]))

    ff = expand(f.copy(), 1000000)
    print(sum(manhatten_dist(g0,g1) for i,g0 in enumerate(ff) for g1 in ff[i+1:]))


if __name__ == "__main__":
    main()

# year 2023
# solution for 11.01: 9274989
# solution for 11.02: 357134560737
