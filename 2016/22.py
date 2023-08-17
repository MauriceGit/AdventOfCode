#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

def pp(cap, w, h, nodes):
    for y in range(h):
        for x in range(w):
            print(f"{nodes[y*w+x]}/{cap[x,y]}\t", end="")
        print()

def main():

    lines = open_data("22.data")[2:]

    cap = dict()
    # [data]
    nodes = [0] * len(lines)
    # [(i, data)]
    contains_source = []

    w = max(ints(l)[0] for l in lines)+1
    h = max(ints(l)[1] for l in lines)+1

    cap = {(tmp[0],tmp[1]): tmp[2] for tmp in map(ints, lines)}
    # have everything in there twice for convenience
    for (x,y), v in list(cap.items()):
        cap[y*w + x] = v

    for (x,y,_,used,_,_) in map(ints, lines):
        nodes[y*w+x] = used
    contains_source.append((w-1, nodes[w-1]))

    pairs = 0
    for i1, u1 in enumerate(nodes):
        for i2, u2 in enumerate(nodes):
            pairs += i1 != i2 and u1 != 0 and u1 <= cap[i2]-u2
    print(pairs)

    # Solved part2 by hand... (using the pp()-function above)
    # It needs 80 moves for the empty node to move to the adjacent node of our source.
    #   The only important thing here is, that there is a "wall" of 4xx nodes that are filled and can never be moved
    #   because the empty node does not have enough space for that much data. So it acts like a blockade we need to move around.
    # Then one move for the source to move one over.
    # From then on, it always takes 4 moves to get the 0 in front and 1 move to actually go there.
    # The target (0,0) is 36 blocks away (straight line). So the solution is:
    # 8 + 1 + 36*(4+1) == 261
    print(261)

if __name__ == "__main__":
    main()

# year 2016
# solution for 22.01: 1034
# solution for 22.02: 261
