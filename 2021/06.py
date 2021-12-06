#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def run(numbers, days):
    fishes = Counter(numbers)
    for minutes in range(days):
            tmp_fishes = fishes.copy()
            for i in range(1,9):
                fishes[i-1] = tmp_fishes[i]
            fishes[8] = tmp_fishes[0]
            fishes[6] += tmp_fishes[0]
    return sum(fishes.values())


def main():

    lines = ints(open_data("06.data")[0])

    print(run(lines, 80))
    print(run(lines, 256))


if __name__ == "__main__":
    main()

# year 2021
# solution for 06.01: 353079
# solution for 06.02: 1605400130036
