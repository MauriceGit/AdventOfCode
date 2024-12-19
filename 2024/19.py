#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

cache = dict()

@cached(cache, key=lambda patterns, design: hashkey(design))
def count_arrangements(patterns, design):
    if design == "":
        return 1

    count = 0
    for p in patterns:
        if design.startswith(p):
            count += count_arrangements(patterns, design[len(p):])
    return count


def main():

    patterns, designs = open_data_groups("19.data")
    patterns = patterns[0].split(", ")

    print(sum(count_arrangements(patterns, design) > 0 for design in designs))
    print(sum(count_arrangements(patterns, design) for design in designs))


if __name__ == "__main__":
    main()

# year 2024
# solution for 19.01: 340
# solution for 19.02: 717561822679428
