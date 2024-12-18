#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def main():

    lines = open_data("18.data")

    width, height = 70, 70
    corrupted = dict()
    for x,y in map(ints, lines[:1024]):
        corrupted[(x,y)] = "#"

    last_path = set()
    for i, (x,y) in enumerate(map(ints, lines[1024:])):
        corrupted[(x,y)] = "#"

        if len(last_path) > 0 and (x,y) not in last_path:
            continue

        def get_neighbors(state, pos):
            for d in dir_list_4():
                tmp = add(pos, d)
                if 0 <= tmp[0] <= width and 0 <= tmp[1] <= height and tmp not in corrupted:
                    yield tmp

        _, dist, path = dijkstra((0, 0), get_neighbors, end_pos=(width, height), use_path=True)
        if i == 0:
            print(dist)
        if dist is None:
            print(f"{x},{y}")
            break
        last_path = set(path)


if __name__ == "__main__":
    main()

# year 2024
# solution for 18.01: 288
# solution for 18.02: 52,5
