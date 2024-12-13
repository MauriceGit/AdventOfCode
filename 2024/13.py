#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

Machine = namedtuple("Machine", "a b dst")

# solves the linear system for n and m (the two unknown multiplation factors)
# and True/False, if those numbers are integer factors (and therefore valid!)
def calc_factors(m, part2=False):
    dstx, dsty = m.dst[0] + (10000000000000 if part2 else 0), m.dst[1] + (10000000000000 if part2 else 0)
    n = (m.b[1]*dstx - m.b[0]*dsty)/ (m.a[0]*m.b[1] - m.a[1]*m.b[0])
    m = (-m.a[1]*dstx + m.a[0]*dsty)/ (m.a[0]*m.b[1] - m.a[1]*m.b[0])
    return n, m, n.is_integer() and m.is_integer()

def main():

    groups = open_data_groups("13.data")
    machines = []
    for g in groups:
        machines.append(Machine(tuple(ints(g[0])), tuple(ints(g[1])), tuple(ints(g[2]))))

    print(sum(ok * int(n*3+m) for n,m,ok in map(calc_factors, machines)))
    print(sum(ok * int(n*3+m) for n,m,ok in map(lambda x: calc_factors(x, part2=True), machines)))


if __name__ == "__main__":
    main()

# year 2024
# solution for 13.01: 29023
# solution for 13.02: 96787395375634
