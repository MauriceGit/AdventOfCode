#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def main():

    lines = open_data("07.data")
    grid = defaultdict(str)
    start = (0,0)
    for y,line in enumerate(lines):
        for x,c in enumerate(line):
            grid[(x,y)] = c
            if c == "S":
                start = (x,y)
                grid[(x,y)] = "."

    # Breath-First-Search. Go every level and track positions instead of going down to the end every single time!
    # pos -> count
    positions = {start: 1}
    count = 0
    for level in range(len(lines)):
        new_positions = dict()
        for p in positions:
            new_ps = []
            if grid[p] == "^":
                new_ps.append(add(p, ( 1,1)))
                new_ps.append(add(p, (-1,1)))
                count += 1
            else:
                new_ps.append(add(p, (0,1)))

            for new_p in new_ps:
                if new_p in new_positions:
                    new_positions[new_p] += positions[p]
                else:
                    new_positions[new_p] = positions[p]
        positions = new_positions

    print(count)
    print(sum(positions.values()))


if __name__ == "__main__":
    main()

# year 2025
# solution for 07.01: 1518
# solution for 07.02: 25489586715621
