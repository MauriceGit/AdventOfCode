#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


fuel_dist = {0:0}
for i in range(1, 2000):
    fuel_dist[i] = fuel_dist[i-1] + i


def run(lines, f):
    best_fuel = 10000000000000000000
    for i in range(min(lines), max(lines)):
        best_fuel = min(best_fuel, sum(f(abs(i-l)) for l in lines))
    return best_fuel


def main():
    lines = ints(open_data("07.data")[0])

    print(run(lines, lambda x: x))
    print(run(lines, lambda x: fuel_dist[x]))


if __name__ == "__main__":
    main()

# year 2021
# solution for 07.01: 351901
# solution for 07.02: 101079875
