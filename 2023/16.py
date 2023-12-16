#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

def energize(dirs, start_p, len_x, len_y):
    energized = set()
    visited = set()

    queue = [start_p]
    heapify(queue)

    while len(queue) > 0:
        old_b = heappop(queue)

        for b in dirs[old_b]:
            x1, x2 = old_b[0][0], b[0][0]
            y1, y2 = old_b[0][1], b[0][1]

            for x in range(min(x1,x2), max(x1,x2)+1):
                for y in range(min(y1,y2), max(y1,y2)+1):
                    energized.add((x,y))

            if b in visited or b[0][0] < 0 or b[0][0] >= len_x or b[0][1] < 0 or b[0][1] >= len_y:
                continue

            visited.add(b)
            heappush(queue, b)

    return len(lfilter(lambda x: 0 <= x[0] < len_x and 0 <= x[1] < len_y, energized))

def next_free(f, positions, valid):
    for p in positions:
        if p in f and f[p] in valid:
            return p
    return p

def main():

    lines = open_data("16.data")

    f = dict()
    for y,line in enumerate(lines):
        for x,c in enumerate(line):
            if c != ".":
                f[(x,y)] = c

    len_x = len(lines[0])
    len_y = len(lines)

    dirs = dict()
    for k, v in f.items():

        u = next_free(f, ((k[0],y) for y in range(k[1]-1, -2, -1)), "/\\-")
        d = next_free(f, ((k[0],y) for y in range(k[1]+1, len_y+1)), "/\\-")
        l = next_free(f, ((x,k[1]) for x in range(k[0]-1, -2, -1)), "/\\|")
        r = next_free(f, ((x,k[1]) for x in range(k[0]+1, len_x+1)), "/\\|")

        match v:
            case "/":
                dirs[(k, (1,0))] = [(u, (0,-1))]
                dirs[(k, (-1,0))] = [(d, (0,1))]
                dirs[(k, (0,1))] = [(l, (-1,0))]
                dirs[(k, (0,-1))] = [(r, (1,0))]
            case "\\":
                dirs[(k, (1,0))] = [(d, (0,1))]
                dirs[(k, (-1,0))] = [(u, (0,-1))]
                dirs[(k, (0,1))] = [(r, (1,0))]
                dirs[(k, (0,-1))] = [(l, (-1,0))]
            case "-":
                dirs[(k, (0,1))] = [(l,(-1,0)), (r,(1,0))]
                dirs[(k, (0,-1))] = [(l,(-1,0)), (r,(1,0))]
            case "|":
                dirs[(k, (1,0))] = [(u,(0,-1)), (d,(0,1))]
                dirs[(k, (-1,0))] = [(u,(0,-1)), (d,(0,1))]

    # starting positions get special handling...
    r = next_free(f, ((x,0) for x in range(0, len_x)), "/\\|")
    dirs[((-1,0), (1,0))] = [(r,(1,0))]

    sl = [((x,-1),(0,1)) for x in range(len(lines[0]))]
    sr = [((x,len(lines)),(0,-1)) for x in range(len(lines[0]))]
    su = [((-1, y),(1,0)) for y in range(len(lines))]
    sd = [((len(lines[0]), y),(-1,0)) for y in range(len(lines))]

    for s in sd:
        r = next_free(f, ((x,s[0][1]) for x in range(0, len_x+1)), "/\\|")
        l = next_free(f, ((x,s[0][1]) for x in range(len_x-1, -2, -1)), "/\\|")
        dirs[((-1,s[0][1]), (1,0))] = [(r,(1,0))]
        dirs[((len_x,s[0][1]), (-1,0))] = [(l,(-1,0))]

    for s in sr:
        u = next_free(f, ((s[0][0],y) for y in range(len_y-1, -2, -1)), "/\\-")
        d = next_free(f, ((s[0][0],y) for y in range(0, len_y+1)), "/\\-")

        dirs[((s[0][0],len_y), (0,-1))] = [(u,(0,-1))]
        dirs[((s[0][0],-1), (0,1))] = [(d,(0,1))]

    print(energize(dirs, ((-1,0), (1,0)), len_x, len_y))
    print(max(energize(dirs, s, len_x, len_y) for s in sl + sr + su + sd))


if __name__ == "__main__":
    main()

# year 2023
# solution for 16.01: 7728
# solution for 16.02: 8061
