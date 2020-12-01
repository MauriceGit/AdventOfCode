#!/usr/bin/env python3.7

from utility import *

def puzzle_1(lines):
    for l in lines:
        for l2 in lines:
            if l+l2 == 2020:
                return l*l2
    return 0

def puzzle_2(lines):
    for l in lines:
        for l2 in lines:
            for l3 in lines:
                if l+l2+l3 == 2020:
                    return l*l2*l3
    return 0

def main():

    lines = open_data("01.data")
    # SHIT
    lines = list(map(int, lines))

    print(puzzle_1(lines))
    print(puzzle_2(lines))

if __name__ == "__main__":
    main()

# solution for 01.01: 299299
# solution for 01.02: 287730716
