#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *

def calc_fuel(diff):
    fuel = 0
    n = 1
    for i in range(diff):
        fuel += n
        n += 1
    return fuel


fuel_dist = dict()
for i in range(2000):
    fuel_dist[i] = calc_fuel(i)


def main():

    lines = ints(open_data("07.data")[0])
    #print(lines)

    #best_pos  = -1
    #best_fuel = 10000000
    #for i in range(min(lines), max(lines)):
    #    fuel = sum(abs(i-l) for l in lines)
    #    if fuel < best_fuel:
    #        best_fuel = fuel
    #        best_pos = i
    #print(best_fuel)

    best_pos  = -1
    best_fuel = 10000000000000000000
    for i in range(min(lines), max(lines)):
        fuel = sum(fuel_dist[abs(i-l)] for l in lines)

        if fuel < best_fuel:
            best_fuel = fuel
            best_pos = i
    print(best_fuel)



if __name__ == "__main__":
    main()

# year 2021
# solution for 07.01: 351901
# solution for 07.02: 101079875
