#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

width  = 50
height = 6

def print_field(s):
    for i in range(height):
        print(format(s[i], "#0{}b".format(width+2))[2:].replace("1", "█").replace("0", " "))

def rot_col(s, x, c):
    tmp = s.copy()
    onebit = np.uint64(1<<(width-x-1))
    for y in range(height):
        s[y] = (s[y] & ~onebit) | (onebit & tmp[(y-c)%height])
    return s

def rot_row(s, y, c):
    firstn = np.uint64(2**c-1)
    s[y] = (s[y] >> np.uint64(c)) | ((s[y] & firstn) << np.uint64(width-c))
    return s

def turn_on(s, w, h):
    mask = np.uint64((2**w-1) << (width-w))
    for i in range(h):
        s[i] |= mask
    return s

def main():

    lines = open_data("08.data")

    screen = np.array([0]*height, dtype=np.uint64)
    for l in lines:
        a, b = ints(l)
        if l.startswith("rect"):
            screen = turn_on(screen, a, b)
        if "row" in l:
            screen = rot_row(screen, a, b)
        if "column" in l:
            screen = rot_col(screen, a, b)

    print(sum(screen[i].bit_count() for i in range(height)))
    print_field(screen)


if __name__ == "__main__":
    main()

# year 2016
# solution for 08.01: 110
# solution for 08.02: ZJHRKCPLYJ
