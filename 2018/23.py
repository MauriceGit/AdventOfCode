#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *

def rotate3fz(p, angle):
    angle = deg_to_rad(angle)
    return (cos(angle)*p[0]-sin(angle)*p[1], sin(angle)*p[0]+cos(angle)*p[1], p[2])
def rotate3fy(p, angle):
    angle = deg_to_rad(angle)
    return (cos(angle)*p[0]+sin(angle)*p[2], p[1], -sin(angle)*p[0]+cos(angle)*p[2])

def dist(b1, b2):
    s = sub3(b1[0], b2[0])
    return abs(s[0])+abs(s[1])+abs(s[2])

def vec_length(s):
    return abs(s[0])+abs(s[1])+abs(s[2])

def cube_intersects(a, b):
    c1 = a[1][0] < b[0][0]
    c2 = b[1][0] < a[0][0]
    c3 = a[1][2] < b[0][2]
    c4 = b[1][2] < a[0][2]
    c5 = a[1][1] < b[0][1]
    c6 = b[1][1] < a[0][1]
    return not(c1 or c2 or c3 or c4 or c5 or c6)

# if a is inside b
def cube_in_cube(a, b):
    x = a[0][0] >= b[0][0] and a[1][0] <= b[1][0]
    y = a[0][1] >= b[0][1] and a[1][1] <= b[1][1]
    z = a[0][2] >= b[0][2] and a[1][2] <= b[1][2]
    return x and y and z

@lru_cache(maxsize=10000000)
def cube_intersection(a, b):
    if not cube_intersects(a, b):
        return None
    if cube_in_cube(a, b):
        return a
    if cube_in_cube(b, a):
        return b

    x0, x1 = max(a[0][0], b[0][0]), min(a[1][0], b[1][0])
    y0, y1 = max(a[0][1], b[0][1]), min(a[1][1], b[1][1])
    z0, z1 = max(a[0][2], b[0][2]), min(a[1][2], b[1][2])

    return ((x0,y0,z0), (x1,y1,z1))

def best_intersection(cubes):

    intersection_counts = []
    best_cubes = []

    for i, c1 in enumerate(cubes):
        cube = c1
        count = 1
        for j, c2 in enumerate(cubes):
            new_cube = cube_intersection(cube, c2)

            if new_cube is not None:
                cube = new_cube
                count += 1

                if intersection_counts == [] or count > intersection_counts[-1]:
                    best_cubes = [cube]
                    intersection_counts = [count]
                elif count == intersection_counts[-1]:
                    best_cubes.append(cube)
                    intersection_counts.append(count)


    return list(zip(best_cubes, intersection_counts))


def best_intersection_2(cubes):
    best_cubes = []

    for i in range(0, len(cubes)):
        found_at_least_one = False
        combs = combinations(cubes, len(cubes)-1-i)
        print(i)
        for quads in combs:
            cube = quads[0]
            found = True
            for q in quads[1:]:
                new_cube = cube_intersection(cube, q)
                if new_cube is None:
                    found = False
                    break
                cube = new_cube

            if found:
                best_cubes.append(cube)

            found_at_least_one = found_at_least_one or found

        if found_at_least_one:
            break

    return best_cubes


def main():

    lines = open_data("23.data")

    nanobots = []
    for l in lines:
        x,y,z,r = ints(l)
        nanobots.append(((x,y,z), r))

    best_bot = max(nanobots, key=lambda x: x[1])

    print(sum(dist(b, best_bot) <= best_bot[1] for b in nanobots))

    for i,b in enumerate(nanobots):
        nanobots[i] = (rotate3fy(rotate3fz(b[0], 45), 45), b[1]/2)

    bots = [((x-r,y-r,z-r), (x+r,y+r,z+r)) for (x,y,z),r in nanobots]

    bots.sort()
    cubes = best_intersection(bots)

    print(len(cubes))
    #cube = cubes[0][0]

    lengths = []
    for cube in cubes:
        #print(cube, count)


        corner1 = cube[0][0]
        corner2 = cube[0][1]
        corner1 = rotate3fz(rotate3fy(cube[0][0], -45), -45)
        corner2 = rotate3fz(rotate3fy(cube[0][1], -45), -45)

        print(corner1, corner2)
        dx, dy, dz = corner2[0]-corner1[0], corner2[1]-corner1[1], corner2[2]-corner1[2]
        corners = [
            corner1,
            corner2,
            add3(corner1, (dx,0,0)),
            add3(corner1, (0,dy,0)),
            add3(corner1, (0,0,dz)),
            add3(corner1, (dx,dy,0)),
            add3(corner1, (dx,0,dz)),
            add3(corner1, (0,dy,dz))
        ]

        best_corner = min(corners, key=vec_length)
        print(vec_length(lmap(int, best_corner)))
        lengths.append(vec_length(lmap(int, best_corner)))

    print(min(lengths))


    # < 156987769
    # > 9645141
if __name__ == "__main__":
    main()

# year 2018
# solution for 23.01: ?
# solution for 23.02: ?
