#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

def connect(f, max_p, p, new_p):
    if 0 <= new_p[0] <= max_p[0] and 0 <= new_p[1] <= max_p[1]:
        f[p].append(new_p)

# line to the left. Returns all encountered symbols
def calc_line_count(path, f, p):
    if p in path:
        return 0

    count = 0
    start_from_up = None
    for i in range(p[0]):
        pp = (i, p[1])
        if pp in path:
            if f[pp] == "|":
                count += 1
            # they start from the left
            if f[pp] in "FL":
                start_from_up = f[pp] == "L"
                count += 1
            if f[pp] == "J" and start_from_up:
                count += 1
            if f[pp] == "7" and not start_from_up:
                count += 1

    return count

def main():

    lines = open_data("10.data")
    max_p = (len(lines[0])-1, len(lines)-1)
    start_p = None

    f = defaultdict(list)
    symbols = dict()
    for y,line in enumerate(lines):
        for x,c in enumerate(line):
            symbols[(x,y)] = c
            match c:
                case "|":
                    connect(f, max_p, (x,y), (x,y-1))
                    connect(f, max_p, (x,y), (x,y+1))
                case "-":
                    connect(f, max_p, (x,y), (x-1,y))
                    connect(f, max_p, (x,y), (x+1,y))
                case "L":
                    connect(f, max_p, (x,y), (x,y-1))
                    connect(f, max_p, (x,y), (x+1,y))
                case "J":
                    connect(f, max_p, (x,y), (x,y-1))
                    connect(f, max_p, (x,y), (x-1,y))
                case "7":
                    connect(f, max_p, (x,y), (x-1,y))
                    connect(f, max_p, (x,y), (x,y+1))
                case "F":
                    connect(f, max_p, (x,y), (x+1,y))
                    connect(f, max_p, (x,y), (x,y+1))
                case "S":
                    start_p = (x,y)


    start_positions = []
    if start_p in f[add(start_p, (0,-1))]:
        start_positions.append(add(start_p, (0,-1)))
    if start_p in f[add(start_p, (0, 1))]:
        start_positions.append(add(start_p, (0, 1)))
    if start_p in f[add(start_p, (-1,0))]:
        start_positions.append(add(start_p, (-1,0)))
    if start_p in f[add(start_p, ( 1,0))]:
        start_positions.append(add(start_p, ( 1,0)))


    State = recordtype("State", "f count path")

    def get_neighbors(state, pos):
        #match state.f[pos]:
        #    case "|": return [add(pos,(0,-1)), add(pos,(0,1))]
        #    case "-": return [add(pos,(-1,0)), add(pos,(1,0))]
        #    case "L": return [add(pos,(0,-1)), add(pos,(1,0))]
        #    case "J": return [add(pos,(0,-1)), add(pos,(-1,0))]
        #    case "7": return [add(pos,(-1,0)), add(pos,(0,1))]
        #    case "F": return [add(pos,(1,0)), add(pos,(0,1))]
        #return []
        return state.f[pos]


    def visit(state, pos, dist, path):
        #if state.f[pos] == "S":
        if start_p in state.f[pos]:
            state.count = max(state.count, dist)
            if dist > 1:
                state.path = path

        return True

    path = []
    max_length = 0
    for p in start_positions:
        state = State(f, 0, [])
        dijkstra(p, get_neighbors, state=state, visit=visit, use_path=True)
        # +2 because we miss the first and the last step!
        max_length = max(max_length, state.count+2)
        if len(state.path) > len(path):
            path = state.path

    print(max_length//2)


    # make sure to substitute the original "S" with the correct pipe symbol!
    ps, pt = path[0], path[-1]
    pp = list(sorted([ps, pt], key=itemgetter(1)))
    if abs(ps[0]-pt[0]) == 2:
        symbols[start_p] = "-"
    if abs(ps[1]-pt[1]) == 2:
        symbols[start_p] = "|"

    if add(start_p, (0,-1)) == pp[0]:
        if add(start_p, (1,0)) == pp[1]:
            symbols[start_p] = "L"
        if add(start_p, (-1,0)) == pp[1]:
            symbols[start_p] = "J"
    if add(start_p, (0,1)) == pp[1]:
        if add(start_p, (1,0)) == pp[0]:
            symbols[start_p] = "F"
        if add(start_p, (-1,0)) == pp[0]:
            symbols[start_p] = "7"


    path = set(path+[start_p])
    print(sum(calc_line_count(path, symbols, k)%2 != 0 for k in symbols.keys()))


if __name__ == "__main__":
    main()

# year 2023
# solution for 10.01: 7063
# solution for 10.02: 589
