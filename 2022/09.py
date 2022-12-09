#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def run(lines, knots):
    visited = set()
    positions = [(0,0) for i in range(knots)]
    for line in lines:
        d, c = line.split(" ")
        for cc in range(int(c)):
            positions[0] = add(positions[0], direction_map()[d])
            for i in range(1, knots):
                dist = manhatten_dist(positions[i-1], positions[i])
                dd = sub(positions[i-1], positions[i])
                if dist >= 3 or dist == 2 and not all(dd):
                    positions[i] = add(positions[i], tuple(map(lambda x: max(-1, min(1, x)), dd)))
            visited.add(positions[-1])
    return len(visited)


def main():

    lines = open_data("09.data")

    print(run(lines, 2))
    print(run(lines, 10))


if __name__ == "__main__":
    main()

# year 2022
# solution for 09.01: 5695
# solution for 09.02: 2434
