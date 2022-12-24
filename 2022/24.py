#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

# set( ((x,y),(dx, dy)), ... )
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

    # (pos, current_i)
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
                #blizzards.add(((x-1,y-1), to_dir[c]))
                #blizzards[(x-1,y-1)] = to_dir[c]
                blizzards[(x-1,y-1)].append(to_dir[c])

    states = [blizzards]
    for i in range(500):
        states.append(simulate(states[-1], field_size))

    print("Done generating.")

        #g = dict()
        #for b, dirs in states[-1].items():
        #    if len(dirs) == 1:
        #        g[b] = to_char[dirs[0]]
        #    else:
        #        g[b] = str(len(dirs))
        #draw_direct(g)

    #return

    #state = {"blizzards": states, "field_size": field_size, "start": start, "end": end}


    def get_neighbors(state, pos):
        #print(pos[1])
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

    if False:
        for p in res[2]:
            g = dict()
            g[(-1,-1)] = "#"
            g[(field_size[0], field_size[1])] = "#"
            for b, dirs in states[p[1]-1].items():
                if len(dirs) == 1:
                    g[b] = to_char[dirs[0]]
                elif len(dirs) > 1:
                    g[b] = str(len(dirs))
                #elif p[0] == b:
                g[p[0]] = "E"
                #print(p[0], b)
            print(f"Minute {p[1]-1}")
            draw_direct(g)

    a = res[1]
    print(a)

    new_start = (end[0], a+1)
    new_end = (start[0], -1)
    state = {"blizzards": states, "field_size": field_size, "end": new_end}
    res = dijkstra(new_start, get_neighbors, state=state, end_pos=new_end)

    b = res[1]
    print(b)

    new_start = (start[0], b+1)
    new_end = (end[0], -1)
    state = {"blizzards": states, "field_size": field_size, "end": new_end}
    res = dijkstra(new_start, get_neighbors, state=state, end_pos=new_end)

    c = res[1]
    print(c)

    print(a+b+c)


    #print(start, end)
    #draw_direct(grid)





if __name__ == "__main__":
    main()

# year 2022
# solution for 24.01: 311
# solution for 24.02: ?
