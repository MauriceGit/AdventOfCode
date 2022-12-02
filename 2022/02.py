#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


rps  = {"A": 0, "B": 1, "C": 2, 0: "X", 1: "Y", 2: "Z"}
ps = {"AX": 4, "BX": 1, "CX": 7, "AY": 8, "BY": 5, "CY": 2, "AZ": 3, "BZ": 9, "CZ": 6}

def chose(l, s):
    return rps[(rps[l]+(-1 if s == "X" else 0 if s == "Y" else 1))%3]

def main():

    lines = open_data("02.data")

    #points = (0,0)
    #for (l,r) in map(lambda x: x.split(" "), lines):
    #    points = add(points, (ps[l+r], ps[l+chose(l, r)]))

    points = reduce(add, map(lambda x: (ps[x[0]+x[1]], ps[x[0]+chose(x[0],x[1])]), map(lambda x: x.split(" "), lines)))

    print(f"{points[0]}\n{points[1]}")


if __name__ == "__main__":
    main()

# year 2022
# solution for 02.01: 14297
# solution for 02.02: 10498
