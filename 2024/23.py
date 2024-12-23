#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

# reduce to sub-group where all members are interconnected!
def reduce_interconnected(connections, group):
    for c1 in group:
        for c2 in group:
            if c1 != c2 and c1 not in connections[c2]:
                sub_g1 = reduce_interconnected(connections, group - {c1})
                sub_g2 = reduce_interconnected(connections, group - {c2})
                if len(sub_g1) > len(sub_g2):
                    return sub_g1
                return sub_g2
    return group


def main():

    computers = lmap(lambda x: x.split("-"), open_data("23.data"))
    connections = defaultdict(set)
    for c1, c2 in computers:
        connections[c1].add(c2)
        connections[c2].add(c1)

    triangles = set()
    largest_set = set()
    for c1, l in connections.items():
        for c2 in l:
            for c3 in l:
                if c3 in connections[c2]:
                    triangles.add(tuple(sorted([c1,c2,c3])))

        tmp = reduce_interconnected(connections, l.copy()) | {c1}
        if len(tmp) > len(largest_set):
            largest_set = tmp

    print(sum(map(lambda x: any(map(lambda y: y.startswith("t"), x)), triangles)))

    print(",".join(sorted(largest_set)))


if __name__ == "__main__":
    main()

# year 2024
# solution for 23.01: 1077
# solution for 23.02: bc,bf,do,dw,dx,ll,ol,qd,sc,ua,xc,yu,zt
