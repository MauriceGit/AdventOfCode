#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def step(right, down, w, h):
    new_right = right.copy()
    for (x,y) in right:
        new_pos = ((x+1)%w, y)
        if new_pos not in right and new_pos not in down:
            new_right.add(new_pos)
            new_right.remove((x,y))
    new_down = down.copy()
    for (x,y) in down:
        new_pos = (x, (y+1)%h)
        if new_pos not in new_right and new_pos not in down:
            new_down.add(new_pos)
            new_down.remove((x,y))
    return new_right, new_down, new_right == right and new_down == down


def main():

    lines = open_data("25.data")

    right = {(x,y) for y,l in enumerate(lines) for x,c in enumerate(l) if c == ">"}
    down  = {(x,y) for y,l in enumerate(lines) for x,c in enumerate(l) if c == "v"}
    w, h = len(lines[0]), len(lines)

    for i in itertools.count():
        right, down, done = step(right, down, w, h)
        if done:
            print(i+1)
            break


if __name__ == "__main__":
    main()

# year 2021
# solution for 25.01: 582
# solution for 25.02: *
