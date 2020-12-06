#!/usr/bin/env python3.7

from utility import *
from functools import reduce
from operator import iconcat

def main():

    groups = open_data_groups("06.data")

    # Puzzle 1
    print(sum(map(len, map(set, [reduce(iconcat, g) for g in groups]))))

    # Puzzle 2
    # sum over the generator object created by the ... for g in groups.
    print(sum(len(reduce(set.intersection, map(set, g))) for g in groups))

if __name__ == "__main__":
    main()

# solution for 06.01: 6680
# solution for 06.02: 3117
