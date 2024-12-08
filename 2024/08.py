#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def calc_antinodes(p1, p2, max_x, max_y, part1=True):
    diff = sub(p2, p1)
    if part1:
        return {add(p2, diff), sub(p1, diff)}

    s = set()
    while 0 <= p2[0] < max_x and 0 <= p2[1] < max_y:
        s.add(p2)
        p2 = add(p2, diff)
    while 0 <= p1[0] < max_x and 0 <= p1[1] < max_y:
        s.add(p1)
        p1 = sub(p1, diff)
    return s


def calc_unique_antinode_count(antennas, max_x, max_y, part1=True):
    antinodes = set()
    for antenna in antennas.values():
        for comb in combinations(antenna, 2):
            antinodes |= calc_antinodes(*comb, max_x, max_y, part1=part1)

    return len(list(filter(lambda x: 0 <= x[0] < max_x and 0 <= x[1] < max_y, antinodes)))


def main():

    lines = open_data("08.data")

    antennas = defaultdict(list)
    max_x, max_y = len(lines[0]), len(lines)

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c != ".":
                antennas[c].append((x, y))

    print(calc_unique_antinode_count(antennas, max_x, max_y))
    print(calc_unique_antinode_count(antennas, max_x, max_y, part1=False))


if __name__ == "__main__":
    main()

# year 2024
# solution for 08.01: 379
# solution for 08.02: 1339
