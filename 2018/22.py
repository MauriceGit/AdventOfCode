#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *
from heapq import heapify, heappop, heappush


def calc_geo_index(pos, target, depth):
    if pos == (0,0):
        return 0
    if pos == target:
        return 0
    if pos[1] == 0:
        return pos[0]*16807
    if pos[0] == 0:
        return pos[1]*48271
    return calc_erosion_level(add(pos,(-1,0)), target, depth) * calc_erosion_level(add(pos,(0,-1)), target, depth)


@lru_cache(maxsize=1000000)
def calc_erosion_level(pos, target, depth):
    return (calc_geo_index(pos, target, depth) + depth) % 20183


def calc_final_erosion_level(pos, target, depth):
    if pos[0] < 0 or pos[1] < 0:
        return -1
    return calc_erosion_level(pos, target, depth) % 3


def bfs(depth, target):

    # 0 == rocky, 1 == wet, 2 == narrow
    # equipment:
    no_tool, torch, climbing_gear = 0, 1, 2
    # (pos, tool) -> distance
    visited = set()
    # (distance, pos, tool)
    queue = [(0, (0,0), torch)]
    target = (target, torch)

    heapify(queue)

    while len(queue) > 0:
        dist, pos, tool = heappop(queue)

        if pos[0] < 0 or pos[1] < 0:
            continue

        terrain = calc_final_erosion_level(pos, target[0], depth)

        # check gear-terrain compatibility
        if terrain == tool:
            continue

        if (pos, tool) == target:
            return dist

        # we don't need to check distance as we are always using the fastest new position anyway!
        if (pos, tool) in visited:
            continue

        visited.add((pos, tool))

        for d in dir_list_4():
            new_pos = add(pos, d)
            new_terrain = calc_final_erosion_level(new_pos, target[0], depth)

            if new_terrain == terrain:
                heappush(queue, (dist+1, new_pos, tool))
            else:
                for new_tool in [no_tool, torch, climbing_gear]:
                    if terrain == new_tool:
                        continue
                    new_dist = 1 + dist + (7 if new_tool != tool else 0)
                    heappush(queue, (new_dist, new_pos, new_tool))

    return -1


def main():

    lines = open_data("22.data")
    depth = ints(lines[0])[0]
    target = tuple(ints(lines[1]))

    print(sum(calc_final_erosion_level((x,y), target, depth) for x in range(target[0]+1) for y in range(target[1]+1)))
    print(bfs(depth, target))


if __name__ == "__main__":
    main()

# year 2018
# solution for 22.01: 7402
# solution for 22.02: 1025
