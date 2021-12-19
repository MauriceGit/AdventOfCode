#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *



def compute_diffs(origin, beacons):
    return [sub(origin, b) for b in beacons]


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


def apply_transformation(transform, v):
    v2 = rotate3d_x(v, count=transform[0])
    v2 = rotate3d_y(v2, count=transform[1])
    v2 = rotate3d_z(v2, count=transform[2])
    return v2

@lru_cache(maxsize=1)
def unique_transformations():
    transforms = set()
    v = (1,2,3)

    # saves: orientation -> transformation
    d = dict()

    for x in range(3,-1,-1):
        for y in range(3,-1,-1):
            for z in range(3,-1,-1):
                v2 = apply_transformation((x,y,z), v)
                transforms.add(v2)
                d[v2] = (x,y,z)

    return [d[t] for t in transforms]


def find_unique_diff(overlap, diff1, diff2):

    for diff in overlap:
        if diff1.count(diff) == 1 and diff2.count(diff) == 1:
            return diff
    return None


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

                overlap = list(set(diff1).intersection(set(diff2_trans)))

                if len(overlap) >= 12:
                    print("FOUND")

                    unique_diff = find_unique_diff(overlap, diff1, diff2_trans)
                    print(unique_diff)

                    p0 = beacons1[diff1.index(unique_diff)]
                    p1 = apply_transformation(transform, beacons2[diff2_trans.index(unique_diff)])

                    print(p0, p1, sub(p0, p1))

                    # center point of beacons2 in the coordinate system of beacons 1!
                    center = sub(p0, p1)

                    return center, transform

    return [], None


def transforms_to_0(keys, sensor):

    if (0, sensor) in keys:
        return (0, sensor)

    for k in keys:
        if k[1] == sensor and k[0] == 0:
            return k
    return None


def bfs(dirs, sensor):

    visited = set()

    queue = [(sensor, [sensor])]

    while len(queue) > 0:

        node, path = queue.pop(0)

        if node == 0:
            return path

        if node in visited:
            continue

        visited.add(node)

        for d in dirs[node]:
            queue.append((d, path + [d]))


    return []




def main():

    groups = open_data_groups("19.data")

    sensors = []
    for g in groups:
        sensors.append([])
        for beacon in g[1:]:
            sensors[-1].append(tuple(ints(beacon)))


    # To find the overlap between sensor 0 and sensor 1:
    # Take every beacon in sensor 1 as origin
    #   Compute all the differences to the beacon origin (sensor 1)
    #   Take every beacon in sensor 2 as origin
    #     Compute all the differences to beacon origin (sensor 2)
    #       For every possible transformation (applied to sensor 2 differences) (24x)
    #
    #         If we have at least 12 equal differences between these sets: len(diff_2.intersection(diff_1))
    #         then those beacons overlap! Save the transformation for sensor 2 for later. That transformation
    #         can be used to move all sensor 2-beacons into sensor 1 coordinate system!
    #
    # Comparisons: 25 * 25 * 24 * 25 + 625 == 375625

    # (sensor_x, sensor_y) -> transform: sensor_y --> sensor_x
    transforms = dict()
    # int -> list: sensor_y --> list_of_sensors where transforms exist in transforms!
    transform_dirs = defaultdict(list)


    #points, transform = find_intersection(sensors[0], sensors[1])
    #return


    #all_points = dict()

    for i, s1 in enumerate(sensors):
        for j, s2 in enumerate(sensors):
            if i != j and (j,i) not in transforms:
                print(i, j)
                center, transform = find_intersection(s1, s2)

                if transform is not None:
                    transforms[(i,j)] = (center, transform)
                    transforms[(j,i)] = (center, transform)
                    transform_dirs[i].append(j)
                    transform_dirs[j].append(i)

                    #all_points[j] = points

    #print(transforms)
    #print(transform_dirs)
    #
    #for p in sorted(all_points[1]):
    #    print(p)


    all_beacons_in_sensor_0_coords = set(sensors[0])

    transformed_beacons = dict()

    for i, s in enumerate(sensors[1:]):
        #print(s)
        points = set(s)
        transform_path = list(reversed(bfs(transform_dirs, i+1)))

        print(transform_path)

        for index in range(len(transform_path)-1):
            a = transform_path[index]
            b = transform_path[index+1]

            center, transform = transforms[(a, b)]

            #center = apply_transformation(transform, center)


            #points = {sub(p, center) for p in points}
            #points = {apply_transformation(transform, p) for p in points}
            #points = {add(p, center) for p in points}

            #print(s[0])
            #print(sub(s[0], center))
            ##print(sub(center, s[0]))
            ##print(add(center, s[0]))
            #
            #print(add(apply_transformation(transform, s[0]), center))
            #print(apply_transformation(transform, sub(s[0], center)))
            #return

            points = {add(apply_transformation(transform, p), center) for p in points}




        #print(points)

        #for p in sorted(points):
        #    print(p)

        #break



        transformed_beacons[i+1] = points
        all_beacons_in_sensor_0_coords = all_beacons_in_sensor_0_coords.union(points)


    #for b in sorted(transformed_beacons[1]):
    #    print(b)

    for b in sorted(all_beacons_in_sensor_0_coords):
        print(b)

    print(len(all_beacons_in_sensor_0_coords))



if __name__ == "__main__":
    main()

# year 2021
# solution for 19.01: ?
# solution for 19.02: ?
