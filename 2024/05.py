#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def find_last_insert_pos(new_update, after, number):
    for i, n in enumerate(new_update):
        # first position that we can insert number, that is valid!
        if n in after[number]:
            return i
    return len(new_update)


def fix_order_median(update, after):
    new_update = []
    for n in update:
        i = find_last_insert_pos(new_update, after, n)
        new_update.insert(i, n)
    return new_update[len(new_update)//2]


def order_ok(update, after):
    for i, n in enumerate(update):
        if set(update[:i]) & set(after[n]) != set():
            return False
    return True


def main():

    ordering, updates = open_data_groups("05.data")

    # list of numbers that must come AFTER the key
    after = defaultdict(list)
    for o in map(ints, ordering):
        after[o[0]].append(o[1])

    p1 = 0
    p2 = 0
    for update in map(ints, updates):
        if order_ok(update, after):
            p1 += update[len(update)//2]
        else:
            p2 += fix_order_median(update, after)

    print(p1)
    print(p2)


if __name__ == "__main__":
    main()

# year 2024
# solution for 05.01: 5374
# solution for 05.02: 4260
