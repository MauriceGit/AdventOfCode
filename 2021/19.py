#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


# 90° around ? axis!
def rotate3d_x(v, count=1):
    if count == 0:
        return v
    return rotate3d_x((v[0], -v[2], v[1]), count-1)
def rotate3d_y(v, count=1):
    if count == 0:
        return v
    return rotate3d_y((v[2], v[1], -v[0]), count-1)
def rotate3d_z(v, count=1):
    if count == 0:
        return v
    return rotate3d_z((-v[1], v[0], v[2]), count-1)


@lru_cache(maxsize=10)
def unique_transformations():
    transforms = set()
    # saves: orientation -> transformation
    d = dict()
    for x in range(3,-1,-1):
        for y in range(3,-1,-1):
            for z in range(3,-1,-1):
                v2 = apply_transformation((x,y,z), (1,2,3))
                transforms.add(v2)
                d[v2] = (x,y,z)
    return [d[t] for t in transforms]


def apply_transformation(transform, v):
    v2 = rotate3d_x(v, count=transform[0])
    v2 = rotate3d_y(v2, count=transform[1])
    v2 = rotate3d_z(v2, count=transform[2])
    return v2


def compute_diffs(origin, beacons):
    return [sub(origin, b) for b in beacons]


def find_intersection(beacons1, beacons2):

    for origin1 in beacons1:
        diff1 = compute_diffs(origin1, beacons1)
        for origin2 in beacons2:
            diff2 = compute_diffs(origin2, beacons2)

            # early return, if it's just not possible!
            tmp1 = set(lmap(manhatten_length, diff1))
            tmp2 = set(lmap(manhatten_length, diff2))
            if len(tmp1.intersection(tmp2)) < 12:
                continue

            for transform in unique_transformations():

                diff2_trans = [apply_transformation(transform, v) for v in diff2]
                if len(list(set(diff1).intersection(set(diff2_trans)))) >= 12:
                    # center point of beacons2 in the coordinate system of beacons 1!
                    center = sub(apply_transformation(transform, origin2), origin1)
                    return center, transform

    return [], None


def main():

    groups = open_data_groups("19.data")

    sensors = []
    for g in groups:
        sensors.append([])
        for beacon in g[1:]:
            sensors[-1].append(tuple(ints(beacon)))

    centers = []
    all_points = set(sensors[0])
    unused_sensors = sensors[1:]
    while len(unused_sensors) > 0:

        points = unused_sensors.pop(0)
        center, transform = find_intersection(all_points, points)

        if transform is not None:
            centers.append(center)
            all_points |= {sub(apply_transformation(transform, p), center) for p in points}
        else:
            unused_sensors.append(points)

    print(len(all_points))
    print(max(map(lambda x: manhatten_dist(x[0],x[1]), combinations(centers, 2))))


if __name__ == "__main__":
    main()

# year 2021
# solution for 19.01: 454
# solution for 19.02: 10813
