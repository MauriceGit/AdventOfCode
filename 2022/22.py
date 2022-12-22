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

def wrap(grid, pos, d):
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

    block_size = 4 # CHANGE !!!!!!!!!
    section = 0
    if pos[1] < block_size:
        section = 1
    elif pos[1] < 2*block_size:
        section = pos[0]//block_size + 2
    else:
        section = (pos[0]-2*block_size)//block_size + 5

    print(f"We are in section {section}")
    bs_min_1 = block_size-1

    if section == 1 and d[0] == -1:
        return (pos[1]+block_size, block_size), (0,1)
    if section == 1 and d[0] == 1:
        return (4*block_size-1, bs_min_1-pos[1] + 2*block_size), (-1,0)
    if section == 1 and d[1] == -1:
        return (bs_min_1-(pos[0]-2*block_size), block_size), (0,1)

    if section == 2 and d[0] == -1:
        return (bs_min_1-(pos[1]-block_size) + 3*block_size, 3*block_size-1), (0,-1)
    if section == 2 and d[1] == -1:
        return (bs_min_1-pos[0] + 2*block_size, 0), (0,1)
    if section == 2 and d[1] == 1:
        return (bs_min_1-pos[0] + 2*block_size, 3*block_size-1), (0,-1)

    if section == 3 and d[1] == -1:
        return (2*block_size, pos[0]-block_size), (1,0)
    if section == 3 and d[1] == 1:
        return (2*block_size, bs_min_1-(pos[0]-block_size) + 2*block_size), (1,0)

    if section == 4 and d[0] == 1:
        return (bs_min_1-(pos[1]-block_size) + 3*block_size, 2*block_size), (0,1)

    if section == 5 and d[0] == -1:
        return (bs_min_1-(pos[1]-2*block_size)+block_size, 2*block_size-1), (0,-1)
    if section == 5 and d[1] == 1:
        return (bs_min_1-(pos[0]-2*block_size), 2*block_size-1), (0,-1)

    if section == 6 and d[0] == 1:
        return (3*block_size-1, bs_min_1-(pos[1]-2*block_size)), (-1,0)
    if section == 6 and d[1] == -1:
        return (3*block_size-1, bs_min_1-(pos[0]-3*block_size) + block_size), (-1,0)
    if section == 6 and d[1] == 1:
        return (0, bs_min_1-(pos[0]-3*block_size) + block_size), (1,0)



def run(grid, commands, pos):
    d = (1,0)
    grid[pos] = {(1,0): ">", (0,1): "v", (-1,0): "<", (0,-1): "^"}[d]
    for c in commands:
        print(f"COMMAND {c}")
        if type(c) == int:
            for i in range(c):
                #print(i)
                print(pos, d)
                #draw(grid, symbols={-1: " ", ".": ".", "#":"#"})

                new_pos = add(pos, d)

                new_pos, new_d = wrap2(grid, new_pos, d)
                print(new_pos, new_d)
                print()

                if grid[new_pos] == ".":
                    pos = new_pos
                    d = new_d

                    grid[new_pos] = {(1,0): ">", (0,1): "v", (-1,0): "<", (0,-1): "^"}[new_d]


                else:
                    break
        else:
            d = rotate(d, c == "R");

    print(d)
    dn = {(1,0): 0, (0,1): 1, (-1,0): 2, (0,-1): 3}[d]

    print(pos[1], pos[0], dn)
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

    print(dirs, n)

    run(grid, dirs, pos)





if __name__ == "__main__":
    main()

# year 2022
# solution for 22.01: ?
# solution for 22.02: ?
