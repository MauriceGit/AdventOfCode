#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def main():
    lines = open_data("02.data")

    possible = {"red": 12, "green": 13, "blue": 14}
    part1 = 0
    part2 = 0

    for line in lines:
        power = {"red": 0, "green": 0, "blue": 0}
        ok = True
        for hand in line.split(": ")[1].split("; "):
            for cube in lmap(lambda x: x.split(" "), hand.split(", ")):
                if possible[cube[1]] < int(cube[0]):
                    ok = False
                power[cube[1]] = max(power[cube[1]], int(cube[0]))
        if ok:
            part1 += int(line.split(":")[0].split(" ")[1])
        part2 += reduce(operator.mul, power.values())

    print(part1)
    print(part2)


if __name__ == "__main__":
    main()

# year 2023
# solution for 02.01: 2101
# solution for 02.02: 58269
