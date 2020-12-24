#!/usr/bin/env python3.7

from utility import *


def parse(l):
    while l != "":
        if l.startswith(("se", "sw", "nw", "ne")):
            yield l[:2]
            l = l[2:]
        else:
            yield l[:1]
            l = l[1:]

# https://www.redblobgames.com/grids/hexagons/
def hex_dirs():
    return {
        "e":  (1, -1, 0),
        "se": (0, -1, 1),
        "sw": (-1, 0, 1),
        "w":  (-1, 1, 0),
        "nw": (0, 1, -1),
        "ne": (1, 0, -1)
    }

def get_pos(tile_dirs):
    return reduce(add3, [hex_dirs()[t] for t in tile_dirs], (0,0,0))


def neighbors(tiles, p):
    return sum([tiles[add3(p, d)] for d in hex_dirs().values()])


def somethingsomething_art_exhibit(tiles, count):

    for i in range(count):

        new_tiles = defaultdict(bool)
        for old_t in list(tiles.keys()):
            for d in hex_dirs().values():
                t = add3(old_t, d)

                adjacent = neighbors(tiles, t)
                if tiles[t] and 1 <= adjacent <= 2:
                    new_tiles[t] = True
                if not tiles[t] and adjacent == 2:
                    new_tiles[t] = True

        tiles = new_tiles

    return tiles


def main():

    lines = open_data("24.data")
    tile_dirs = lmap(list, lmap(parse, lines))

    tiles = defaultdict(bool)

    for dirs in tile_dirs:
        tiles[get_pos(dirs)] = not tiles[get_pos(dirs)]

    print(sum(tiles.values()))

    print(sum(somethingsomething_art_exhibit(tiles, 100).values()))


if __name__ == "__main__":
    main()

# solution for 24.01: 288
# solution for 24.02: 4002
