#!/usr/bin/env python3.7

from utility import *
import re

def puzzle(lines, puzzle_1):
    dirs = direction_map("EWNS")

    pos = (0,0)
    faceing = (1,0) if puzzle_1 else (10,1)

    for l in lines:

        r = re.match(r"([NSEWLRF])(\d+)", l)
        command, count = r.group(1), int(r.group(2))

        if command in "NSEW":
            if puzzle_1:
                pos = add(pos, mul(dirs[command], count))
            else:
                faceing = add(faceing, mul(dirs[command], count))

        if command in "LR":
            faceing = rotate(faceing, command == "L", count=count//90)

        if command == "F":
            if puzzle_1:
                pos = add(pos, mul(faceing, count))
            else:
                for i in range(count):
                    pos = add(pos, faceing)

    return abs(pos[0])+abs(pos[1])


def main():

    lines = open_data("12.data")

    print(puzzle(lines, True))
    print(puzzle(lines, False))


if __name__ == "__main__":
    main()

# solution for 12.01: 441
# solution for 12.02: 40014
