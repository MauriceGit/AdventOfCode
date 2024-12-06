#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


# Just simulate it again until we find a loop... There got to be a better way...
def has_loop(field, p, d, visited, max_x, max_y):
    new_visited = dict()
    while True:
        while add(p, d) in field:
            d = rotate(d, True)
        p = add(p, d)
        if p[0] < 0 or p[1] < 0 or p[0] > max_x or p[1] > max_y:
            return False
        if visited.get(p, None) == d or new_visited.get(p, None) == d:
            return True
        new_visited[p] = d


def run(field, p, d):
    start_p = p
    visited = {p: d}
    max_x = max(map(lambda x: x[0], field.keys()))
    max_y = max(map(lambda x: x[1], field.keys()))
    loops_found = 0

    while True:
        while add(p, d) in field:
            d = rotate(d, True)

        # we cannot add a blocker on a path we have already been on, otherwise
        # we wouldn't even get here!
        if add(p, d) not in visited and add(p, d) != start_p:
            loops_found += has_loop(field | {add(p, d):"#"}, p, d, visited, max_x, max_y)

        p = add(p, d)
        if p[0] < 0 or p[1] < 0 or p[0] > max_x or p[1] > max_y:
            return len(visited), loops_found
        visited[p] = d


def main():

    lines = open_data("06.data")

    field = dict()
    p = (0,0)
    d = (0, -1)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "^":
                p = (x,y)
            if c == "#":
                field[(x, y)] = c

    p1, p2 = run(field, p, d)
    print(p1)
    print(p2)


if __name__ == "__main__":
    main()

# year 2024
# solution for 06.01: 5409
# solution for 06.02: 2022
