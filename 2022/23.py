#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

dirs = dict(zip(["E", "W", "S", "N", "SE", "NW", "SW", "NE"], dir_list_8()))
to_i = {d: i for i,d in enumerate(dirs.keys())}

def propose_move(elves, elve, rot):
    check = [add(elve, dirs[k]) not in elves for k in dirs.keys()]
    if all(check):
        return None

    for i in range(4):
        match (i+rot)%4:
            case 0:
                if check[to_i["N"]] and check[to_i["NE"]] and check[to_i["NW"]]:
                    return add(elve, dirs["N"])
            case 1:
                if check[to_i["S"]] and check[to_i["SE"]] and check[to_i["SW"]]:
                    return add(elve, dirs["S"])
            case 2:
                if check[to_i["W"]] and check[to_i["NW"]] and check[to_i["SW"]]:
                    return add(elve, dirs["W"])
            case 3:
                if check[to_i["E"]] and check[to_i["NE"]] and check[to_i["SE"]]:
                    return add(elve, dirs["E"])
    return None


def next_round(elves, i):
    proposed = dict()
    spots = defaultdict(int)

    # First halve round
    for e in elves:
        p = propose_move(elves, e, i)
        proposed[e] = p if p is not None else e
        spots[proposed[e]] += 1

    someone_moved = False
    for e in list(elves):
        if spots[proposed[e]] == 1:
            elves.remove(e)
            elves.add(proposed[e])
            someone_moved = someone_moved or proposed[e] != e

    return elves, not someone_moved


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
