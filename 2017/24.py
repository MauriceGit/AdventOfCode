#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def find_path(components, last_pin, current_strength, current_path, part2):
    max_strength = current_strength
    best_path = current_path
    for c in components:
        if last_pin not in c:
            continue
        pin_out = c[1] if c[0] == last_pin else c[0]
        s, path = find_path(components - {c}, pin_out, current_strength+sum(c), current_path + [c], part2)

        part2_ok = part2 and (len(path) > len(best_path) or len(path) == len(best_path) and s > max_strength)
        if not part2 and s > max_strength or part2_ok:
            max_strength = s
            best_path = path
    return max_strength, best_path


def main():
    components = set(lmap(lambda x: tuple(map(int, x.split("/"))), open_data("24.data")))

    print(find_path(components, 0, 0, [], False)[0])
    print(find_path(components, 0, 0, [], True)[0])


if __name__ == "__main__":
    main()

# year 2017
# solution for 24.01: 1695
# solution for 24.02: 1673
