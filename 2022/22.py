#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


# returns (lower, upper) bounds for one specific row/col
def find_grid_edge(grid, x=None, y=None):
    # search horizontal/row
    if x != None:
        mi = min(filter(lambda a: a[0] == x, grid.keys()), key=lambda a: a[1])
        ma = max(filter(lambda a: a[0] == x, grid.keys()), key=lambda a: a[1])
        return mi, ma
    # search column
    elif y != None:
        mi = min(filter(lambda a: a[1] == y, grid.keys()), key=lambda a: a[0])
        ma = max(filter(lambda a: a[1] == y, grid.keys()), key=lambda a: a[0])
        return mi, ma


def wrap1(grid, pos, d):
    if pos in grid:
        return pos, d
    # wrap around
    if d[0] == 0:
        low, up = find_grid_edge(grid, x=pos[0])
        if d[1] == 1:
            return low, d
        else:
            return up, d
    else:
        low, up = find_grid_edge(grid, y=pos[1])
        if d[0] == 1:
            return low, d
        else:
            return up, d


def wrap2(grid, pos, d):
    if pos in grid:
        return pos, d

    pos = sub(pos, d)

    block_size = 50
    section = 0
    if pos[1] < block_size and pos[0] < 2*block_size:
        section = 1
    elif pos[1] < block_size and pos[0] >= 2*block_size:
        section = 2
    elif pos[1] < 2*block_size:
        section = 3
    elif pos[1] < 3*block_size and pos[0] < block_size:
        section = 4
    elif pos[1] < 3*block_size and pos[0] >= block_size:
        section = 5
    else:
        section = 6

    bs_min_1 = block_size-1

    # min/max for each block
    min_x1, max_x1, min_y1, max_y1 = block_size, None, 0, None
    min_x2, max_x2, min_y2, max_y2 = None, 3*block_size-1, 0, block_size-1
    min_x3, max_x3, min_y3, max_y3 = block_size, 2*block_size-1, None, None
    min_x4, max_x4, min_y4, max_y4 = 0, None, 2*block_size, None
    min_x5, max_x5, min_y5, max_y5 = None, 2*block_size-1, None, 3*block_size-1
    min_x6, max_x6, min_y6, max_y6 = 0, block_size-1, None, 4*block_size-1

    if section == 1 and d[0] == -1:
        return (min_x4, bs_min_1-pos[1]+2*block_size), (1,0)
    if section == 1 and d[1] == -1:
        return (min_x6, pos[0]-block_size + 3*block_size), (1,0)

    if section == 2 and d[0] == 1:
        return (max_x5, bs_min_1-pos[1] + 2*block_size), (-1,0)
    if section == 2 and d[1] == -1:
        return (pos[0]-2*block_size, max_y6), (0,-1)
    if section == 2 and d[1] == 1:
        return (max_x3, pos[0]-2*block_size + block_size), (-1,0)

    if section == 3 and d[0] == -1:
        return (pos[1]-block_size, min_y4), (0,1)
    if section == 3 and d[0] == 1:
        return (pos[1]-block_size+2*block_size, max_y2), (0,-1)

    if section == 4 and d[0] == -1:
        return (min_x1, bs_min_1-(pos[1]-2*block_size)), (1,0)
    if section == 4 and d[1] == -1:
        return (min_x3, pos[0]+block_size), (1,0)

    if section == 5 and d[0] == 1:
        return (max_x2, bs_min_1-(pos[1]-2*block_size)), (-1,0)
    if section == 5 and d[1] == 1:
        return (max_x6, pos[0]-block_size + 3*block_size), (-1,0)

    if section == 6 and d[0] == -1:
        return (pos[1]-3*block_size+block_size, min_y1), (0,1)
    if section == 6 and d[0] == 1:
        return (pos[1]-3*block_size+block_size, max_y5), (0,-1)
    if section == 6 and d[1] == 1:
        return (pos[0]+2*block_size, min_y2), (0,1)


def run(grid, commands, pos, wrapper):
    d = (1,0)
    for c in commands:
        if type(c) == int:
            for i in range(c):
                new_pos = add(pos, d)
                new_pos, new_d = wrapper(grid, new_pos, d)
                if grid[new_pos] != "#":
                    pos = new_pos
                    d = new_d
                else:
                    break
        else:
            d = rotate(d, c == "R");

    dn = {(1,0): 0, (0,1): 1, (-1,0): 2, (0,-1): 3}[d]
    print((pos[1]+1)*1000 + (pos[0]+1)*4 + dn)


def main():

    lines, pw = open_data_groups("22.data")

    found_start = False
    pos = (0,0)
    d = (1,0)
    grid = dict()
    for y,l in enumerate(lines):
        for x, c in enumerate(l):
            if c in ".#":
                if y == 0 and c == "." and not found_start:
                    pos = (x,y)
                    found_start = True
                grid[(x,y)] = c

    dirs = []
    n = ""
    for c in pw[0]:
        if c in "0123456789":
            n += c
        if c in "RL":
            dirs.append(int(n))
            dirs.append(c)
            n = ""
    dirs.append(int(n))

    run(grid, dirs, pos, wrap1)
    run(grid, dirs, pos, wrap2)


if __name__ == "__main__":
    main()

# year 2022
# solution for 22.01: ?
# solution for 22.02:  >/!= 19237, < 59307
