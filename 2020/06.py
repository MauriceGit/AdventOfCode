#!/usr/bin/env python3.7

from utility import *
from functools import reduce

def main():

    groups = open("06.data", "r").read().split("\n\n")

    # Puzzle 1
    print(sum(map(len, map(set, map(lambda x: x.replace("\n", ""), groups)))))

    # Puzzle 2
    groups = map(lambda x: map(set, x.splitlines()), groups)
    print(sum([len(reduce(set.intersection, g)) for g in groups]))


if __name__ == "__main__":
    main()

# solution for 06.01: 6680
# solution for 06.02: 3117
