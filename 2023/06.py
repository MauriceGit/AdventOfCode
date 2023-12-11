#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def won(race, i):
    return i*(race[0]-i) > race[1]


def find(race, start, end, f=won):
    if start >= end-1:
        return start
    if f(race, start+(end-start)//2):
        return find(race, start, start+(end-start)//2, f)
    return find(race, start+(end-start)//2, end, f)


def main():

    lines = open_data("06.data")

    not_won = lambda a,b: not won(a,b)
    race = zip(*map(ints, lines))
    print(reduce(operator.mul, (find(r, 0, r[0], f=not_won)-find(r, 0, r[0]) for r in race)))

    r = lmap(lambda x: ints(x.replace(" ", ""))[0], lines)
    print(find(r, 0, r[0], f=not_won) - find(r, 0, r[0]))


if __name__ == "__main__":
    main()

# year 2023
# solution for 06.01: 1159152
# solution for 06.02: 41513103
