#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def parse(l):
    return [1 if e == '#' else 0 for e in l]


def pp(plants, generation):

    mi = min(filter(lambda x: plants[x], plants.keys()))
    ma = max(filter(lambda x: plants[x], plants.keys()))
    print(generation, mi, ma, end=" - ")
    for k in range(mi, ma+1):
        print("#" if plants[k] else ".", end="")
    print("")


def run(plants, gen, count):

    min_index = -2
    max_index = len(plants)+2
    for g in range(count):
        copy = plants.copy()
        mi = min(filter(lambda x: plants[x], plants.keys()))
        ma = max(filter(lambda x: plants[x], plants.keys()))
        for i in range(mi-2, ma+3):
            t = (plants[i-2], plants[i-1], plants[i], plants[i+1], plants[i+2])
            copy[i] = 0 if t not in gen else gen[t]
        plants = copy

        min_index -= 2
        max_index += 2

    return plants


def main():

    init, updates = open_data_groups("12.data")

    plants = defaultdict(int, {i: e for i,e in enumerate(parse(init[0].split(": ")[1]))})

    gen = dict()
    for u in updates:
        s, t = u.split(" => ")
        gen[tuple(parse(s))] = parse(t[0])[0]

    plants_copy = run(plants, gen, 20)
    print(sum([e[0] if e[1] else 0 for e in plants_copy.items()]))

    # mutations are stable after ~108 generations, 200 is just to be safe.
    generations = 200
    plants = run(plants, gen, generations)
    tmp_res = sum([e[0] if e[1] else 0 for e in plants.items()])
    print((50000000000-generations)*sum(plants.values()) + tmp_res)


if __name__ == "__main__":
    main()

# year 2018
# solution for 12.01: 1733
# solution for 12.02: 1000000000508
