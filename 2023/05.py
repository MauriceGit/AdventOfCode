#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


# returns the maximal length that can be mapped between the given units
def convert_type(seed, length, unit, to, convert):
    for r in convert[(unit, to)]:
        if r[1] <= seed < r[1]+r[2]:
            return r[0]+(seed-r[1]), min(length, (r[1]+r[2]) - seed)
    return seed, 1


# only the very first number matters for the mapping (as they are increasing!)
# so increase the seed as much as the range conversion allows!
def find_locations(seed, length, conversion_possible, convert):
    unit = "seed"
    while unit != "location":
        to = conversion_possible[unit]
        seed, found_length = convert_type(seed, length, unit, to, convert)
        length = min(length, found_length)
        unit = to
    return seed, length


def main():

    groups = open_data_groups("05.data")

    seeds = ints(groups[0][0])
    groups = groups[1:]

    convert = defaultdict(list)

    conversion_possible = dict()

    for g in groups:
        fr = g[0].split("-to-")[0]
        to = g[0].split("-to-")[1].split(" ")[0]
        conversion_possible[fr] = to
        for l in g[1:]:
            convert[(fr, to)].append(ints(l))

    # add a number ranges for all areas that are not specified!
    for k,v in list(convert.items()):
        tmp_list = list(sorted(v, key=lambda x: x[1]))
        add = []
        if tmp_list[0][1] != 0:
            add.append([0, 0, tmp_list[1][1]])
        for i in range(len(tmp_list)-1):
            l1 = tmp_list[i]
            l2 = tmp_list[i+1]
            if l1[1]+l1[2] < l2[1]:
                add.append([l1[1]+l1[2], l1[1]+l1[2], l2[1]-(l1[1]+l1[2])])
            convert[k] = tmp_list + add

    print(min(find_locations(seed, 1, conversion_possible, convert)[0] for seed in seeds))

    min_seed_loc = -1
    for i in range(0, len(seeds), 2):
        seed, length = seeds[i], seeds[i+1]
        all_length = 0
        while True:
            loc, found_length = find_locations(seed, length, conversion_possible, convert)
            min_seed_loc = loc if min_seed_loc < 0 else min(min_seed_loc, loc)
            seed += found_length
            all_length += found_length
            if all_length >= length:
                break
    print(min_seed_loc)


if __name__ == "__main__":
    main()

# year 2023
# solution for 05.01: 165788812
# solution for 05.02: 1928058
