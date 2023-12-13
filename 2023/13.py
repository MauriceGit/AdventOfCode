#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

# creates two lists of rows that should be identical. Lists are flattened, zipped and compared!
def is_center_row(p1, i):
    lu = [c for l in (p1[j] for j in range(i, -1, -1)) for c in l]
    ld = [c for l in (p1[j] for j in range(i+1,len(p1))) for c in l]
    return min(len(lu), len(ld)) - sum(l==r for l,r in zip(lu, ld))


def find_center(p1, score=100, result=0):
    for i in range(0, len(p1)-1):
        if is_center_row(p1, i) == result:
            return (i+1)*score
    return find_center(lmap(lambda x: "".join(x), zip(*p1[::-1])), score=1, result=result)


def main():

    groups = open_data_groups("13.data")

    print(sum(find_center(g, result=0) for g in groups))
    print(sum(find_center(g, result=1) for g in groups))


if __name__ == "__main__":
    main()

# year 2023
# solution for 13.01: 30487
# solution for 13.02: 31954
