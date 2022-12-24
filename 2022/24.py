#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

def simulate(blizzards, field_size):

    new_blizzards = defaultdict(list)

    for b, dirs in blizzards.items():
        for d in dirs:
            p = add(b, d)
            new_b = (p[0]%field_size[0], p[1]%field_size[1])
            new_blizzards[new_b].append(d)

    return new_blizzards


def main():

    lines = open_data("24.data")

    to_dir = {"<": (-1,0), ">": (1,0), "^": (0,-1), "v": (0,1)}
    to_char = dict(map(reversed, to_dir.items()))

    start = ((0,0), 1)
    end = ((0,0), -1)
    blizzards = defaultdict(list)
    field_size = (len(lines[0])-2, len(lines)-2)
    for y,l in enumerate(lines):
        for x,c in enumerate(l):
            if y == 0 and c == ".":
                start = ((x-1,y-1), 1)
            if y == len(lines)-1 and c == ".":
                end = ((x-1,y-1), -1)
            if c not in ".#":
                blizzards[(x-1,y-1)].append(to_dir[c])

    states = [blizzards]
    for i in range(1000):
        states.append(simulate(states[-1], field_size))

    def get_neighbors(state, pos):
        blizzard = state["blizzards"][pos[1]]
        fs = state["field_size"]
        end = state["end"]
        positions = []
        pos, i = pos[0], pos[1]
        if pos not in blizzard:
            positions.append((pos, i+1))

        for d in dir_list_4():
            p = add(pos, d)
            if p not in blizzard and 0 <= p[0] < field_size[0] and 0 <= p[1] < field_size[1]:
                positions.append((p, i+1))
            if p == end[0]:
                return [end]
        return positions


    state = {"blizzards": states, "field_size": field_size, "start": start, "end": end}
    res = dijkstra(start, get_neighbors, state=state, end_pos=end)
    a = res[1]
    print(a)

    new_start = (end[0], a+1)
    new_end = (start[0], -1)
    state = {"blizzards": states, "field_size": field_size, "end": new_end}
    res = dijkstra(new_start, get_neighbors, state=state, end_pos=new_end)
    b = res[1]
    new_start = (start[0], a+b+1)
    new_end = (end[0], -1)
    state = {"blizzards": states, "field_size": field_size, "end": new_end}
    res = dijkstra(new_start, get_neighbors, state=state, end_pos=new_end)
    c = res[1]

    print(a+b+c)


if __name__ == "__main__":
    main()

# year 2022
# solution for 24.01: 311
# solution for 24.02: 869
