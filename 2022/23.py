#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

class Dir(IntEnum):
    E = 0
    W = 1
    S = 2
    N = 3
    SE = 4
    NW = 5
    SW = 6
    NE = 7

# order is important (same as Dir enum)! ["E", "W", "S", "N", "SE", "NW", "SW", "NE"]
dirs = dir_list_8()

def propose_move(elves, elve, rot):
    check = [add(elve, d) not in elves for d in dirs]
    if all(check):
        return None, None

    for i in range(4):
        match (i+rot)%4:
            case 0:
                if check[Dir.N] and check[Dir.NE] and check[Dir.NW]:
                    return add(elve, dirs[Dir.N]), dirs[Dir.N]
            case 1:
                if check[Dir.S] and check[Dir.SE] and check[Dir.SW]:
                    return add(elve, dirs[Dir.S]), dirs[Dir.S]
            case 2:
                if check[Dir.W] and check[Dir.NW] and check[Dir.SW]:
                    return add(elve, dirs[Dir.W]), dirs[Dir.W]
            case 3:
                if check[Dir.E] and check[Dir.NE] and check[Dir.SE]:
                    return add(elve, dirs[Dir.E]), dirs[Dir.E]
    return None, None


def next_round(elves, i):
    someone_moved = 0
    cpy = elves.copy()

    for e in cpy:
        p, d = propose_move(cpy, e, i)

        if p in elves:
            # could only have come from the opposite side, so we just push him back!
            elves.add(add(p, d))
            elves.remove(p)
            someone_moved -= 1
        elif p != None:
            elves.add(p)
            elves.remove(e)
            someone_moved += 1

    return elves, someone_moved == 0


def main():

    lines = open_data("23.data")

    elves = set()
    for y,l in enumerate(lines):
        for x,c in enumerate(l):
            if c == "#":
                elves.add((x,y))

    #draw_direct({p:'#' for p in elves} | {(0,0): '.', (5,5): '.'})
    for i in itertools.count():
        elves, done = next_round(elves, i)

        if i == 9:
            min_x = min(elves, key=lambda x: x[0])[0]
            max_x = max(elves, key=lambda x: x[0])[0]+1
            min_y = min(elves, key=lambda x: x[1])[1]
            max_y = max(elves, key=lambda x: x[1])[1]+1
            print((max_x-min_x)*(max_y-min_y) - len(elves))
        if done:
            print(i+1)
            break


if __name__ == "__main__":
    main()

# year 2022
# solution for 23.01: 4172
# solution for 23.02: 942
