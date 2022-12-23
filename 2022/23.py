#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

dirs = dict(zip(["E", "W", "S", "N", "SE", "NW", "SW", "NE"], dir_list_8()))

def propose_move(elves, elve, i):
    if len({add(elve, dirs[d]) for d in dirs.keys()} & elves) == 0:
        return None

    steps = deque([None, None, None, None])
    if len(elves & {add(elve, dirs["N"]), add(elve, dirs["NE"]), add(elve, dirs["NW"])}) == 0:
        steps[0] = add(elve, dirs["N"])
    if len(elves & {add(elve, dirs["S"]), add(elve, dirs["SE"]), add(elve, dirs["SW"])}) == 0:
        steps[1] = add(elve, dirs["S"])
    if len(elves & {add(elve, dirs["W"]), add(elve, dirs["NW"]), add(elve, dirs["SW"])}) == 0:
        steps[2] = add(elve, dirs["W"])
    if len(elves & {add(elve, dirs["E"]), add(elve, dirs["NE"]), add(elve, dirs["SE"])}) == 0:
        steps[3] = add(elve, dirs["E"])
    steps.rotate(-i)
    for s in steps:
        if s != None:
            return s
    return None

def next_round(elves, i):
    proposed = dict()
    spots = defaultdict(int)

    # First halve round
    for e in elves:
        p = propose_move(elves, e, i)
        proposed[e] = p if p is not None else e
        spots[proposed[e]] += 1

    new_elves = elves.copy()
    someone_moved = False
    for e in elves:
        if spots[proposed[e]] == 1:
            new_elves.remove(e)
            new_elves.add(proposed[e])
            someone_moved = someone_moved or proposed[e] != e

    return new_elves, not someone_moved


def main():

    lines = open_data("23.data")

    elves = set()
    for y,l in enumerate(lines):
        for x,c in enumerate(l):
            if c == "#":
                elves.add((x,y))

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
