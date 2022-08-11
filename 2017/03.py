#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def num(n):
    return sum(8*i for i in range(1,n+1))+2


def find_base_round(target):
    base = 0
    while num(base) <= target:
        base += 1
    return base-1


def calc_additional_steps(start_n, incr, target):
    step_diff = (((target-start_n)+1)%(incr-1))
    if step_diff <= incr//2:
        return step_diff
    return (incr//2-(step_diff-incr//2))


def calc_steps(target):
    base_round = find_base_round(target)
    a = num(base_round)
    b = num(base_round+1)-1
    return 2*(base_round+1) - calc_additional_steps(a, (b-a)//4 + 2, target)


def fill_loop(target):

    d = defaultdict(int)
    p = (0,0)
    d[p] = 1

    while True:
        if not d[add(p,(0,1))] and d[add(p,(-1,0))]:
            p = add(p, (0,1))
        elif not d[add(p,(-1,0))] and d[add(p,(0,-1))]:
            p = add(p, (-1,0))
        elif not d[add(p,(0,-1))] and d[add(p,(1,0))]:
            p = add(p, (0,-1))
        else:
            p = add(p, (1,0))

        d[p] = sum(d[add(p, _d)] for _d in dir_list_8())

        if d[p] > target:
            return d[p]


def main():

    lines = open_data("03.data")

    print(calc_steps(ints(lines)[0]))
    print(fill_loop(ints(lines)[0]))


if __name__ == "__main__":
    main()

# year 2017
# solution for 03.01: 419
# solution for 03.02: 295229
