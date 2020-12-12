#!/usr/bin/env python3.7

from utility import *

def puzzle(lines, puzzle_1):
    dirs = direction_map("EWNS")

    pos = (0,0)
    facing = (1,0) if puzzle_1 else (10,1)

    for l in lines:

        r = re.match(r"([NSEWLRF])(\d+)", l)
        command, count = r.group(1), int(r.group(2))

        if command in "NSEW":
            if puzzle_1:
                pos = add(pos, mul(dirs[command], count))
            else:
                facing = add(facing, mul(dirs[command], count))

        if command in "LR":
            facing = rotate(facing, command == "L", count=count//90)

        if command == "F":
            pos = add(pos, mul(facing, count))

    return abs(pos[0])+abs(pos[1])


def main():

    lines = open_data("12.data")

    print(puzzle(lines, True))
    print(puzzle(lines, False))


if __name__ == "__main__":
    main()

# solution for 12.01: 441
# solution for 12.02: 40014
