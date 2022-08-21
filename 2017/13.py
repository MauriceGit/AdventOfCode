#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def run(layers, delay, part2):
    severity = 0
    for key in layers.keys():
        if (key+delay) % ((layers[key]-1)*2) == 0:
            if part2:
                return False, 0
            severity += key*layers[key]
    return True, severity


def main():
    lines = open_data("13.data")

    layers = dict(map(ints, lines))

    print(run(layers, 0, False)[1])

    for delay in itertools.count():
        if run(layers, delay, True)[0]:
            print(delay)
            break


if __name__ == "__main__":
    main()

# year 2017
# solution for 13.01: 1640
# solution for 13.02: 3960702
