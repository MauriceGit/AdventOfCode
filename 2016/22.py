#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def pp(w, h, nodes):
    for y in range(h):
        print("(" if y == 0 else " ", end="")
        for x in range(w):
            d = nodes[y*w+x]
            c = "0" if d == 0 else ("G" if (x,y) == (w-1,0) else ("*" if (x,y) == (0,0) else "."))
            print("#" if d > 400 else c, end=")" if (x,y) == (0,0) else " ")
        print()


def get_neighbors(cap, nodes, w, h, pos):
    empty, data = pos

    e = (empty%w, empty//w)
    s = (data%w, data//w)

    for d in dir_list_4():
        new_e = add(e, d)
        if 0 <= new_e[0] < w and 0 <= new_e[1] < h and nodes[new_e[1]*w+new_e[0]] <= cap[e]:
            yield (new_e[1]*w+new_e[0], data if new_e != s else empty)


def heuristic(node, w):
    empty, data = node
    ex, ey = empty%w, empty//w
    dx, dy = data%w, data//w
    # minus 1 because they can never be on the same position but just adjacent. The value needs to be 0 at the target.
    return (abs(dx-ex) + abs(dy-ey))-1 + (dx + dy)


def run(cap, nodes, w, h):

    empty_node = [i for i in range(w*h) if nodes[i] == 0][0]
    data_node = w-1
    pos = (empty_node, data_node)
    queue = [(0, 0, pos)]
    heapify(queue)
    visited = set()

    while len(queue) > 0:
        _, dist, pos = heappop(queue)
        (empty, data) = pos
        if data == 0:
            return dist

        if pos in visited:
            continue
        visited.add(pos)

        for n in get_neighbors(cap, nodes, w, h, pos):
            heappush(queue, (heuristic(n, w), dist+1, n))

    return 0


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

    #pp(w, h, nodes)
    # Solved part2 by hand... (using the pp()-function above)
    # It needs 80 moves for the empty node to move to the adjacent node of our source.
    #   The only important thing here is, that there is a "wall" of 4xx nodes that are filled and can never be moved
    #   because the empty node does not have enough space for that much data. So it acts like a blockade we need to move around.
    # Then one move for the source to move one over.
    # From then on, it always takes 4 moves to get the 0 in front and 1 move to actually go there.
    # The target (0,0) is 36 blocks away (straight line). So the solution is:
    # 81 + 36*5 == 261
    #print(261)

    # Now correctly solved with A* and a heuristic involving the empty node and source data node.
    print(run(cap, nodes, w, h))


if __name__ == "__main__":
    main()

# year 2016
# solution for 22.01: 1034
# solution for 22.02: 261
