#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def main():

    lines = open_data("04.data")

    numbers_won = []
    points = 0
    for line in lines:
        numbers_won.append(len(set(ints(line.split("|")[0])[1:]).intersection(set(ints(line.split("|")[1])))))
        points += 2**(numbers_won[-1]-1) if numbers_won[-1] != 0 else 0
    print(points)

    # we already have one card each!
    won = defaultdict(lambda: 1)
    # build the tree up from the bottom!
    for i in range(len(lines)-1, -1, -1):
        for c in range(1, numbers_won[i]+1):
            won[i] += won[i+c]
    print(sum(won.values()))


if __name__ == "__main__":
    main()

# year 2023
# solution for 04.01: 26914
# solution for 04.02: 13080971
