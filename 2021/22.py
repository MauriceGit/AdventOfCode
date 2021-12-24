#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *

Cube = recordtype("Cube", "x0 x1 y0 y1 z0 z1")



def diff_cube_left(c0, c1):
    return Cube(min(c0.x0, c1.x0), max(c0.x0, c1.x0)-1, min(c0.y0, c1.y0), max(c0.y0, c1.y0)-1, min(c0.z0, c1.z0), max(c0.z0, c1.z0)-1)
def diff_cube_right(c0, c1):
    return Cube(min(c0.x1, c1.x1)+1, max(c0.x1, c1.x1), min(c0.y1, c1.y1)+1, max(c0.y1, c1.y1), min(c0.z1, c1.z1)+1, max(c0.z1, c1.z1))

def overlap_region(c0, c1):
    return Cube(max(c0.x0, c1.x0), min(c0.x1, c1.x1), max(c0.y0, c1.y0), min(c0.y1, c1.y1), max(c0.z0, c1.z0), min(c0.z1, c1.z1))

def other_overlaps(c0, c1):
    return [
        # OK! 1 in drawing
        Cube(min(c0.x0, c1.x0), max(c0.x0, c1.x0)-1, max(c0.y0, c1.y0), min(c0.y1, c1.y1), max(c0.z0, c1.z0), min(c0.z1, c1.z1)),
        # OK! 2 in drawing
        Cube(min(c0.x1, c1.x1)+1, max(c0.x1, c1.x1), max(c0.y0, c1.y0), min(c0.y1, c1.y1), max(c0.z0, c1.z0), min(c0.z1, c1.z1)),

        # OK! 3 in drawing
        Cube(max(c0.x0, c1.x0), min(c0.x1, c1.x1), min(c0.y0, c1.y0), max(c0.y0, c1.y0)-1, max(c0.z0, c1.z0), min(c0.z1, c1.z1)),
        # OK! 4 in drawing
        Cube(max(c0.x0, c1.x0), min(c0.x1, c1.x1), min(c0.y1, c1.y1)+1, max(c0.y1, c1.y1), max(c0.z0, c1.z0), min(c0.z1, c1.z1)),

        # OK! Not in drawing
        Cube(max(c0.x0, c1.x0), min(c0.x1, c1.x1), max(c0.y0, c1.y0), min(c0.y1, c1.y1), min(c0.z0, c1.z0), max(c0.z0, c1.z0)-1),
        Cube(max(c0.x0, c1.x0), min(c0.x1, c1.x1), max(c0.y0, c1.y0), min(c0.y1, c1.y1), min(c0.z1, c1.z1)+1, max(c0.z1, c1.z1))
    ]






def cubes_have_overlap(c0, c1):

    #return volume(calc_center(c0, c1)) > 0

    b1 = c0.x1 < c1.x0 or c1.x1 < c0.x0
    b2 = c0.y1 < c1.y0 or c1.y1 < c0.y0
    b3 = c0.z1 < c1.z0 or c1.z1 < c0.z0
    return not(b1 or b2 or b3)

def volume(c):
    if c is None:
        return 0
    return ((c.x1+1)-c.x0) * ((c.y1+1)-c.y0) * ((c.z1+1)-c.z0)

def volumes(cs):
    return sum(map(volume, cs))

def calc_bottom(c0, c1):

    #return Cube(min(c0.x0, c1.x0), min(c0.x1, c1.x1), min(c0.y0, c1.y0), max(c0.y0, c1.y0)-1, min(c0.z0, c1.z0), min(c0.z1, c1.z1))

    if c0.y0 < c1.y0:
        return Cube(c0.x0, c0.x1, c0.y0, c1.y0-1, c0.z0, c0.z1)
    elif c1.y0 < c0.y0:
        return calc_bottom(c1, c0)

    return None


def calc_top(c0, c1):

    #return Cube(max(c0.x0, c1.x0), max(c0.x1, c1.x1), min(c0.y1, c1.y1)+1, max(c0.y1, c1.y1), max(c0.z0, c1.z0), max(c0.z1, c1.z1))

    if c0.y1 > c1.y1:
        return Cube(c0.x0, c0.x1, c1.y1+1, c0.y1, c0.z0, c0.z1)
    elif c1.y1 > c0.y1:
        return calc_top(c1, c0)
    return None


def calc_left(c0, c1):

    #return Cube(min(c0.x0, c1.x0), max(c0.x0, c1.x0)-1, min(c0.y0, c1.y0)+1, min(c0.y1, c1.y1), min(c0.z0, c1.z0), min(c0.z1, c1.z1))

    if c0.x0 < c1.x0:
        y0_offset = 0 if c0.y0 >= c1.y0 else 1
        y1_offset = 0 if c0.y1 <= c1.y1 else 1
        z0_offset = 0 if c0.z0 >= c1.z0 else 1
        z1_offset = 0 if c0.z1 <= c1.z1 else 1
        return Cube(c0.x0, c1.x0-1, c0.y0+y0_offset, c0.y1-y1_offset, c0.z0+z0_offset, c0.z1-z1_offset)
    elif c1.x0 < c0.x0:
        return calc_left(c1, c0)
    return None


def calc_right(c0, c1):

    #return Cube(min(c0.x1, c1.x1)+1, max(c0.x1, c1.x1), max(c0.y0, c1.y0), max(c0.y1, c1.y1)-1, max(c0.z0, c1.z0), max(c0.z1, c1.z1))

    if c0.x1 > c1.x1:
        y0_offset = 0 if c0.y0 >= c1.y0 else 1
        y1_offset = 0 if c0.y1 <= c1.y1 else 1
        z0_offset = 0 if c0.z0 >= c1.z0 else 1
        z1_offset = 0 if c0.z1 <= c1.z1 else 1
        return Cube(c1.x1+1, c0.x1, c0.y0+y0_offset, c0.y1-y1_offset, c0.z0+z0_offset, c0.z1-z1_offset)
    elif c1.x1 > c0.x1:
        return calc_right(c1, c0)
    return None


def calc_front(c0, c1):

    #return Cube(max(c0.x0, c1.x0), min(c0.x1, c1.x1), max(c0.y0, c1.y0), min(c0.y1, c1.y1), min(c0.z0, c1.z0), max(c0.z0, c1.z0)-1)

    if c0.z0 < c1.z0:
        y0_offset = 0 if c0.y0 >= c1.y0 else 1
        y1_offset = 0 if c0.y1 <= c1.y1 else 1
        return Cube(c0.x0, c0.x1, c0.y0+y0_offset, c0.y1-y1_offset, c0.z0, c1.z0-1)
    elif c1.z0 < c0.z0:
        return calc_front(c1, c0)
    return None


def calc_back(c0, c1):

    #return Cube(max(c0.x0, c1.x0), min(c0.x1, c1.x1), max(c0.y0, c1.y0), min(c0.y1, c1.y1), min(c0.z1, c1.z1)+1, max(c0.z1, c1.z1))

    if c0.z1 > c1.z1:
        y0_offset = 0 if c0.y0 >= c1.y0 else 1
        y1_offset = 0 if c0.y1 <= c1.y1 else 1
        return Cube(c0.x0, c0.x1, c0.y0+y0_offset, c0.y1-y1_offset, c1.z1+1, c0.z1)
    elif c1.z1 > c0.z1:
        return calc_back(c1, c0)
    return None


def calc_center(c0, c1):
    return Cube(max(c0.x0, c1.x0), min(c0.x1, c1.x1), max(c0.y0, c1.y0), min(c0.y1, c1.y1), max(c0.z0, c1.z0), min(c0.z1, c1.z1))

def overlaps(c0, c1):
    print()

    cs = []
    def append_cube(c):
        if c is not None:
            cs.append(c)
        return c
    bottom = append_cube(calc_bottom(c0, c1))
    top    = append_cube(calc_top(c0, c1))
    left   = append_cube(calc_left(c0, c1))
    right  = append_cube(calc_right(c0, c1))
    front  = append_cube(calc_front(c0, c1))
    back   = append_cube(calc_back(c0, c1))
    center = calc_center(c0, c1)

    print("bottom: {} -> {}".format(bottom, volume(bottom)))
    print("top   : {} -> {}".format(top, volume(top)))
    print("left  : {} -> {}".format(left, volume(left)))
    print("right : {} -> {}".format(right, volume(right)))
    print("front : {} -> {}".format(front, volume(front)))
    print("back  : {} -> {}".format(back, volume(back)))
    print("center: {} -> {}".format(center, volume(center)))

    #cs = [bottom, top, left, right, front, back]

    belong_to_c0 = lfilter(lambda x: cubes_have_overlap(x, c0), cs)
    belong_to_c1 = lfilter(lambda x: cubes_have_overlap(x, c1), cs)

    return belong_to_c0, belong_to_c1, center


def cube_within_cube(c0, c1):
    return c0.x0 >= c1.x0 and c0.x1 <= c1.x1 and c0.y0 >= c1.y0 and c0.y1 <= c1.y1 and c0.z0 >= c1.z0 and c0.z1 <= c1.z1

def main():

    lines = open_data("22.data")


    grid = defaultdict(int)
    for l in lines:
        x0,x1,y0,y1,z0,z1 = ints(l)
        on = l.startswith("on")
        if min(x0,y0,z0) >= -50 and max(x1,y1,z1) <= 50:
            for x in range(x0,x1+1):
                for y in range(y0,y1+1):
                    for z in range(z0,z1+1):
                        grid[(x,y,z)] = int(on)

    print(len(lfilter(lambda x: x==1, grid.values())))



    c0 = Cube(x0=10, x1=12, y0=10, y1=10, z0=10, z1=12)
    c1 = Cube(x0=9, x1=11, y0=9, y1=11, z0=9, z1=11)
    print("Intersect current cube: {} with new cube {}".format(c0, c1))
    only_c0, only_c1, center = overlaps(c0, c1)


    print("Belonging to c0:")
    for c in only_c0:
        print(c, volume(c))
    #print("Belonging to c1:")
    #for c in only_c1:
    #    print(c, volume(c))
    print("Center:")
    print(center, volume(center))

    print("difference in volume: {}".format(volume(center)))

    print("sanity check: {} == {}".format(volume(c0), volumes(only_c0)+volume(center)))


    #return


    cubes = []
    for l in lines[:2]:
        x0,x1,y0,y1,z0,z1 = ints(l)
        on = l.startswith("on")
        cube = Cube(x0,x1,y0,y1,z0,z1)
        has_overlapped = False

        print("=========================================================")
        print("Add new cube: {} --> {}".format(cube, "ON" if on else "OFF"))

        for c in cubes:
            print(c)


        new_cubes = []
        remove_cubes = []
        for i in range(len(cubes)):

            current_cube = cubes[i]
            if cubes_have_overlap(current_cube, cube):


                if cube_within_cube(current_cube, cube):
                    if on:
                        cubes[i] = cube
                    remove_cubes.append(i)
                    continue
                if on and cube_within_cube(cube, current_cube):
                    continue

                remove_cubes.append(i)

                print("Intersect current cube: {} with new cube {}".format(current_cube, cube))

                only_c0, only_c1, center = overlaps(current_cube, cube)



                print("Belonging to c0:")
                for c in only_c0:
                    print(c, volume(c))
                #print("Belonging to c1:")
                #for c in only_c1:
                #    print(c, volume(c))
                print("Center:")
                print(center, volume(center))

                print("difference in volume: {}".format(volume(center)))

                print("sanity check: {} == {}".format(volume(current_cube), volumes(only_c0)+volume(center)))

                #cubes.extend(only_c0)
                new_cubes.extend(only_c0)

                # c should always be on!
                if on:
                    #cubes.extend(only_c1)
                    #cubes.append(center)
                    new_cubes.extend(only_c1)
                    new_cubes.append(center)

                has_overlapped = True

        #for c in remove_cubes:
        #    del cubes[cubes.index(c)]

        for i in sorted(remove_cubes, reverse=True):
            del cubes[i]
        cubes.extend(new_cubes)

        if not has_overlapped:
            cubes.append(cube)

        print("\nAfter this round, there are: {} cubes turned on!\n".format(sum(map(volume, cubes))))



    print("final cubes: ")
    print(sum(map(volume, cubes)))








if __name__ == "__main__":
    main()

# year 2021
# solution for 22.01: ?
# solution for 22.02: ?
