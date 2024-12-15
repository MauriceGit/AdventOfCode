#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

d_map = direction_map("><v^")
inv_d_map = {v: k for k,v in d_map.items()}


def can_move(f, pos, d, p1=False):
    new_p = add(pos, d)

    if new_p not in f:
        return True
    if f[new_p] == "#":
        return False
    if inv_d_map[d] in "v^":
        all_new_p = [new_p, add(new_p, ((1,0) if f[new_p] == "[" else (-1,0)))]
        for new_p in ([new_p] if p1 else all_new_p):
            if not can_move(f, new_p, d, p1=p1):
                return False
        return True

    return can_move(f, new_p, d, p1=p1)

def exec_move(f, pos, d, p1=False):
    if pos not in f:
        return

    new_p = add(pos, d)

    if inv_d_map[d] in "v^":
        all_p = [pos, add(pos, ((1,0) if f[pos] == "[" else (-1,0)))]
        all_new_p = [add(p, d) for p in all_p]
        for old_p, new_p in ([(pos, new_p)] if p1 else zip(all_p, all_new_p)):
            exec_move(f, new_p, d, p1=p1)
            f[new_p] = f[old_p]
            del f[old_p]
    else:
        exec_move(f, new_p, d, p1=p1)
        f[new_p] = f[pos]
        del f[pos]


def move_all(f, pos, movements, p1=False):
    for move in movements:
        if can_move(f, pos, move, p1=p1):
            exec_move(f, add(pos, move), move, p1=p1)
            pos = add(pos, move)


def gps_sum(f, c="O"):
    return sum(map(lambda x: 100*x[1]+x[0], filter(lambda x: f[x] == c, f.keys())))

def main():

    lines, movements = open_data_groups("15.data")
    movements = lmap(lambda x: d_map[x], "".join(movements))
    f = dict()
    pos_p1 = (0,0)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c in "O#":
                f[(x, y)] = c
            if c == "@":
                pos_p1 = (x,y)


    pos_p2 = (pos_p1[0]*2, pos_p1[1])
    new_f = dict()
    for k,v in f.items():
        k = (k[0]*2, k[1])
        if v == "#":
            new_f[k] = v
            new_f[add(k, (1,0))] = v
        if v == "O":
            new_f[k] = "["
            new_f[add(k, (1,0))] = "]"


    move_all(f, pos_p1, movements, p1=True)
    print(gps_sum(f))

    move_all(new_f, pos_p2, movements)
    print(gps_sum(new_f, c="["))


if __name__ == "__main__":
    main()

# year 2024
# solution for 15.01: 1515788
# solution for 15.02: 1516544
