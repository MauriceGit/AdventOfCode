#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

State = recordtype("State", "f count path")

# line to the left. Returns all encountered symbols
def is_inside_path(path, f, p):
    if p in path:
        return False

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

    return count%2 != 0

def get_starting_positions(symbols, start_p):
    if symbols[add(start_p, (0,-1))] in "|7F":
        yield add(start_p, (0,-1))
    if symbols[add(start_p, (0,1))] in "|LJ":
        yield add(start_p, (0, 1))
    if symbols[add(start_p, (-1,0))] in "-LF":
        yield add(start_p, (-1,0))
    if symbols[add(start_p, (1,0))] in "-7J":
        yield add(start_p, ( 1,0))

# replace the 'S' symbol with the correct pipe symbol
def fix_s_symbol(symbols, path, start_p):
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


def main():

    lines = open_data("10.data")

    symbols = {(x,y): c for y,line in enumerate(lines) for x,c in enumerate(line)}
    start_p = lfilter(lambda x: x[1] == "S", symbols.items())[0][0]

    def get_neighbors(state, pos):
        if pos not in state.f:
            return []
        match state.f[pos]:
            case "|": return [add(pos,(0,-1)), add(pos,(0,1))]
            case "-": return [add(pos,(-1,0)), add(pos,(1,0))]
            case "L": return [add(pos,(0,-1)), add(pos,(1,0))]
            case "J": return [add(pos,(0,-1)), add(pos,(-1,0))]
            case "7": return [add(pos,(-1,0)), add(pos,(0,1))]
            case "F": return [add(pos,(1,0)), add(pos,(0,1))]
        return []

    def visit(state, pos, dist, path):
        if start_p in get_neighbors(state, pos):
            state.count = max(state.count, dist)
            if dist > 1:
                state.path = path
        return True

    path = []
    max_length = 0
    for p in get_starting_positions(symbols, start_p):
        state = State(symbols, 0, [])
        dijkstra(p, get_neighbors, state=state, visit=visit, use_path=True)
        # +2 because we miss the first and the last step!
        max_length = max(max_length, state.count+2)
        if len(state.path) > len(path):
            path = state.path
    print(max_length//2)

    # make sure to substitute the original "S" with the correct pipe symbol!
    fix_s_symbol(symbols, path, start_p)

    path = set(path+[start_p])
    print(sum(is_inside_path(path, symbols, k) for k in symbols.keys()))


if __name__ == "__main__":
    main()

# year 2023
# solution for 10.01: 7063
# solution for 10.02: 589
