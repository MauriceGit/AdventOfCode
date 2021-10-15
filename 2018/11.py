#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *

cache = dict()
row_cache = dict()
col_cache = dict()

def calc_level(x, y, sn):
    return ((((((x+1)+10) * (y+1)) + sn) * ((x+1)+10))//100)%10 - 5


def calc_power_levels(grid, sn):
    for x, row in enumerate(grid):
        for y, col in enumerate(row):
            grid[x][y] = calc_level(x, y, sn)


def get_row(grid, x, y, length):

    if (x,y,length) in row_cache:
        return row_cache[(x,y,length)]

    if length == 1:
        return grid[x][y]

    s = get_row(grid, x, y, length-1) + grid[x+length-1][y]
    row_cache[(x,y,length)] = s
    return s


def get_col(grid, x, y, length):

    if (x,y,length) in col_cache:
        return col_cache[(x,y,length)]

    if length == 1:
        return grid[x][y]

    s = get_col(grid, x, y, length-1) + grid[x][y+length-1]
    col_cache[(x,y,length)] = s
    return s


# find the square one size smaller and add the row/col manually.
# That way the calls will be cached and reused later
def find_max_at_cached(grid, x, y, size):
    if (x,y,size) in cache:
        return cache[(x,y,size)]

    if size == 1:
        return grid[x][y]

    s = find_max_at_cached(grid, x, y, size-1)
    s += get_row(grid, x, y+size-1, size)
    s += get_col(grid, x+size-1, y, size)

    cache[(x,y,size)] = s

    return s


def find_max(grid, size):

    max_level = 0
    max_x, max_y = -1, -1

    for x in range(300-(size-1)):
        for y in range(300-(size-1)):
            level = find_max_at_cached(grid, x, y, size)
            if level > max_level:
                max_x, max_y = x+1, y+1
                max_level = level

    return max_level, (max_x, max_y)

def find_n_max(grid):
    max_level = 0
    max_coord = (0,0)
    max_size  = 0
    for size in range(1, 300):
        l = find_max(grid, size)
        if l[0] > max_level:
            max_level = l[0]
            max_coord = l[1]
            max_size = size

    return max_level, (*max_coord, max_size)

def main():

    sn = ints(open_data("11.data")[0])[0]

    grid = [[0]*300 for i in range(300)]

    calc_power_levels(grid, sn)
    print("{},{}".format(*find_max(grid, 3)[1]))
    print("{},{},{}".format(*find_n_max(grid)[1]))


if __name__ == "__main__":
    main()

# year 2018
# solution for 11.01: 20,43
# solution for 11.02: 233,271,13
