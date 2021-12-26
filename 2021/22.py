#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


Cube = recordtype("Cube", "x0 x1 y0 y1 z0 z1 children")


def cubes_have_overlap(c0, c1):
    b1 = c0.x1 < c1.x0 or c1.x1 < c0.x0
    b2 = c0.y1 < c1.y0 or c1.y1 < c0.y0
    b3 = c0.z1 < c1.z0 or c1.z1 < c0.z0
    return not(b1 or b2 or b3)


def calc_top(c0, c1):

    if c0.y1 > c1.y1:
        return Cube(c0.x0, c0.x1, c1.y1+1, c0.y1, c0.z0, c0.z1, [])
    elif c1.y1 > c0.y1:
        return calc_top(c1, c0)
    return None


def calc_bottom(c0, c1):

    if c0.y0 < c1.y0:
        return Cube(c0.x0, c0.x1, c0.y0, c1.y0-1, c0.z0, c0.z1, [])
    elif c1.y0 < c0.y0:
        return calc_bottom(c1, c0)
    return None


def calc_front(c0, c1):

    if c0.z0 < c1.z0:
        y0_offset = 0 if c0.y0 >= c1.y0 else c1.y0-c0.y0
        y1_offset = 0 if c0.y1 <= c1.y1 else c0.y1-c1.y1
        return Cube(c0.x0, c0.x1, c0.y0+y0_offset, c0.y1-y1_offset, c0.z0, c1.z0-1, [])
    elif c1.z0 < c0.z0:
        return calc_front(c1, c0)
    return None


def calc_back(c0, c1):

    if c0.z1 > c1.z1:
        y0_offset = 0 if c0.y0 >= c1.y0 else c1.y0-c0.y0
        y1_offset = 0 if c0.y1 <= c1.y1 else c0.y1-c1.y1
        return Cube(c0.x0, c0.x1, c0.y0+y0_offset, c0.y1-y1_offset, c1.z1+1, c0.z1, [])
    elif c1.z1 > c0.z1:
        return calc_back(c1, c0)
    return None


def calc_left(c0, c1):

    if c0.x0 < c1.x0:
        y0_offset = 0 if c0.y0 >= c1.y0 else c1.y0-c0.y0
        y1_offset = 0 if c0.y1 <= c1.y1 else c0.y1-c1.y1
        z0_offset = 0 if c0.z0 >= c1.z0 else c1.z0-c0.z0
        z1_offset = 0 if c0.z1 <= c1.z1 else c0.z1-c1.z1
        return Cube(c0.x0, c1.x0-1, c0.y0+y0_offset, c0.y1-y1_offset, c0.z0+z0_offset, c0.z1-z1_offset, [])
    elif c1.x0 < c0.x0:
        return calc_left(c1, c0)
    return None


def calc_right(c0, c1):

    if c0.x1 > c1.x1:
        y0_offset = 0 if c0.y0 >= c1.y0 else c1.y0-c0.y0
        y1_offset = 0 if c0.y1 <= c1.y1 else c0.y1-c1.y1
        z0_offset = 0 if c0.z0 >= c1.z0 else c1.z0-c0.z0
        z1_offset = 0 if c0.z1 <= c1.z1 else c0.z1-c1.z1
        return Cube(c1.x1+1, c0.x1, c0.y0+y0_offset, c0.y1-y1_offset, c0.z0+z0_offset, c0.z1-z1_offset, [])
    elif c1.x1 > c0.x1:
        return calc_right(c1, c0)
    return None


def overlaps(c0, c1):
    cs = [
        calc_bottom(c0, c1), # bottom
        calc_top(c0, c1),    # top
        calc_left(c0, c1),   # left
        calc_right(c0, c1),  # right
        calc_front(c0, c1),  # front
        calc_back(c0, c1)    # back
    ]
    return lfilter(lambda x: x is not None and cubes_have_overlap(x, c0), cs)


def calc_volume(c):
    if len(c.children) == 0:
        return ((c.x1+1)-c.x0) * ((c.y1+1)-c.y0) * ((c.z1+1)-c.z0)
    return sum(calc_volume(cc) for cc in c.children)


# c0 is within c1
def cube_within_cube(c0, c1):
    return c0.x0 >= c1.x0 and c0.x1 <= c1.x1 and c0.y0 >= c1.y0 and c0.y1 <= c1.y1 and c0.z0 >= c1.z0 and c0.z1 <= c1.z1


def update_cube(cube, new_cube, on):

    if not cubes_have_overlap(cube, new_cube):
        return cube, False

    # recursive descent for cube children!
    if len(cube.children) > 0:
        delete_indices = []
        for i, c in enumerate(cube.children):
            tmp_c, del_c0 = update_cube(c, new_cube, on)
            if del_c0:
                delete_indices.append(i)
            else:
                cube.children[i] = tmp_c
        for i in sorted(delete_indices, reverse=True):
            del cube.children[i]
        return cube, len(cube.children) == 0

    # leaf node!
    c0 = overlaps(cube, new_cube)

    if cube_within_cube(cube, new_cube):
        return cube, True

    cube.children = c0

    return cube, len(c0) == 0


def calc_on_cubes(lines, part_1=False):

    if part_1:
        lines = lfilter(lambda x: min(ints(x)) >= -50 and max(ints(x)) <= 50, lines)

    cubes = []
    for l in lines:
        x0,x1,y0,y1,z0,z1 = ints(l)
        on = l.startswith("on")
        cube = Cube(x0,x1,y0,y1,z0,z1, [])

        delete_indices = []
        for i,c in enumerate(cubes):
            tmp_c, del_c0 = update_cube(c, cube, on)
            if del_c0:
                delete_indices.append(i)
            else:
                cubes[i] = tmp_c
        for i in sorted(delete_indices, reverse=True):
            del cubes[i]

        if on:
            cubes.append(cube)

    return sum(map(calc_volume, cubes))


def main():

    lines = open_data("22.data")
    print(calc_on_cubes(lines, part_1=True))
    print(calc_on_cubes(lines))


if __name__ == "__main__":
    main()

# year 2021
# solution for 22.01: 652209
# solution for 22.02: 1217808640648260
