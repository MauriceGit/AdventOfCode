#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

dirs = dict(zip(["E", "W", "S", "N", "SE", "NW", "SW", "NE"], dir_list_8()))

def calc_move(elves, elve, rot):

    ok = lambda keys: all(add(elve, dirs[k]) not in elves for k in keys)

    for i in range(4):
        match (i+rot)%4:
            case 0:
                if ok(["N", "NE", "NW"]):
                    return add(elve, dirs["N"])
            case 1:
                if ok(["S", "SE", "SW"]):
                    return add(elve, dirs["S"])
            case 2:
                if ok(["W", "NW", "SW"]):
                    return add(elve, dirs["W"])
            case 3:
                if ok(["E", "NE", "SE"]):
                    return add(elve, dirs["E"])
    return None


def propose_move(elves, elve, i):
    if all(add(elve, k) not in elves for k in dirs.values()):
        return None

    return calc_move(elves, elve, i)

def next_round(elves, i):
    proposed = dict()
    spots = defaultdict(int)

    # First halve round
    for e in elves.keys():
        p = propose_move(elves, e, i)
        proposed[e] = p if p is not None else e
        spots[proposed[e]] += 1

    someone_moved = False
    for e in list(elves.keys()):
        if spots[proposed[e]] == 1:
            del elves[e]
            elves[proposed[e]] = "#"
            someone_moved = someone_moved or proposed[e] != e

    return elves, not someone_moved


def main():

    lines = open_data("23.data")

    elves = dict()
    for y,l in enumerate(lines):
        for x,c in enumerate(l):
            if c == "#":
                elves[(x,y)] = c


    for i in itertools.count():
        elves, done = next_round(elves, i)

        if i == 9:
            min_x = min(elves.keys(), key=lambda x: x[0])[0]
            max_x = max(elves.keys(), key=lambda x: x[0])[0]+1
            min_y = min(elves.keys(), key=lambda x: x[1])[1]
            max_y = max(elves.keys(), key=lambda x: x[1])[1]+1
            print((max_x-min_x)*(max_y-min_y) - len(elves))
        if done:
            print(i+1)
            break


if __name__ == "__main__":
    main()

# year 2022
# solution for 23.01: 4172
# solution for 23.02: 942
