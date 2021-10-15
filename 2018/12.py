#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def parse(l):
    return [1 if e == '#' else 0 for e in l]


def run(plants, gen, count):

    min_index = 0
    max_index = len(plants)
    for i in range(count):
        copy = plants.copy()
        for i in range(min_index, max_index):
            copy[i] = gen[(plants[i-2], plants[i-1], plants[i], plants[i+1], plants[i+2])]
        plants = copy

        min_index -= 2
        max_index += 2






def main():

    init, updates = open_data_groups("12.data")

    plants = defaultdict(int, {i: e for i,e in enumerate(parse(init[0].split(": ")[1]))})

    gen = dict()
    for u in updates:
        s, t = u.split(" => ")
        gen[tuple(parse(s))] = parse(t[0])[0]

    run(plants, gen, 20)

    print(plants)
    print(gen)

    print(sum([e[0] if e[1] else 0 for e in plants.items()]))




    # not 714. Higher

if __name__ == "__main__":
    main()

# year 2018
# solution for 12.01: ?
# solution for 12.02: ?
