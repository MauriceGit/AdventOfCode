#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def step(field):
    queue = []
    for k in field:
        field[k] += 1
        if field[k] > 9:
            queue.append(k)

    flash = 0
    while len(queue) > 0:
        k = queue.pop(0)
        flash += 1
        field[k] = 0

        for d in dir_list_8():
            new_p = add(d, k)
            if new_p in field and 0 < field[new_p] <= 9:
                field[new_p] += 1
                if field[new_p] > 9:
                    queue.append(new_p)

    return flash


def main():

    lines = open_data("11.data")

    field = {(x,y): int(v) for y,l in enumerate(lines) for x,v in enumerate(l)}

    print(sum(step(field) for i in range(100)))

    for i in count():
        if step(field) == 100:
            print(101+i)
            break


if __name__ == "__main__":
    main()

# year 2021
# solution for 11.01: 1729
# solution for 11.02: 237
