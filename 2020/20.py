#!/usr/bin/env python3.7

from utility import *
from enum import Enum

Tile = namedtuple("Tile", "id l r u d")

# Change to 9, 3 for testdata.
tile_count = 144
side_tile_count = 12

g_transform = dict()

t2i = {
    "R0"    : 1 ,
    "R0_FY" : 2 ,
    "R0_FX" : 3 ,
    "R1"    : 4 ,
    "R1_FY" : 5 ,
    "R1_FX" : 6 ,
    "R2"    : 7 ,
    "R2_FY" : 8 ,
    "R2_FX" : 9 ,
    "R3"    : 10,
    "R3_FY" : 11,
    "R3_FX" : 12
}
i2t = {v: k for k,v in t2i.items()}

def h(v, rev):
    if rev:
        return hash(v[::-1])
    return hash(v)

def get_l(t, rev=False):
    return h(tuple([t[i] for i in range(0, 100, 10)]), rev)
def get_r(t, rev=False):
    return h(tuple([t[i+9] for i in range(0, 100, 10)]), rev)
def get_u(t, rev=False):
    return h(tuple(t[:10]), rev)
def get_d(t, rev=False):
    return h(tuple(t[-10:]), rev)


# rev is the axis in the other direction (flipped)
def all_combinations(key, l, r, u, d, rev_l, rev_r, rev_u, rev_d):

    res = list({
        Tile(key, l,r,u,d),
        # flipped y
        Tile(key, rev_l,rev_r,d,u),
        # flipped x
        Tile(key, r,l,rev_u,rev_d),
        # rot 1x
        Tile(key, d, u, rev_l, rev_r),
        # rot 1x flipped y
        Tile(key, rev_d, rev_u, rev_r, rev_l),
        # rot 1x flipped x
        Tile(key, u, d, l, r),
        # rot 2x
        Tile(key, rev_r, rev_l, rev_d, rev_u),
        # rot 2x flipped y
        Tile(key, r, l, rev_u, rev_d),
        # rot 2x flipped x
        Tile(key, rev_l, rev_r, d, u),
        # rot 3x
        Tile(key, rev_u, rev_d, r, l),
        # rot 3x flipped y
        Tile(key, u, d, l, r),
        # rot 3x flipped x
        Tile(key, rev_d, rev_u, rev_r, rev_l),
    })

    # For some reasone, I can NOT put another thing into the namedtuple.
    # The runtime goes from 4s to > 10 minutes (cancelled after that).
    g_transform[Tile(key, l,r,u,d)] = t2i["R0"]
    g_transform[Tile(key, rev_l,rev_r,d,u)] = t2i["R0_FY"]
    g_transform[Tile(key, r,l,rev_u,rev_d)] = t2i["R0_FX"]
    g_transform[Tile(key, d, u, rev_l, rev_r)] = t2i["R1"]
    g_transform[Tile(key, rev_d, rev_u, rev_r, rev_l)] = t2i["R1_FY"]
    g_transform[Tile(key, u, d, l, r)] = t2i["R1_FX"]
    g_transform[Tile(key, rev_r, rev_l, rev_d, rev_u)] = t2i["R2"]
    g_transform[Tile(key, r, l, rev_u, rev_d)] = t2i["R2_FY"]
    g_transform[Tile(key, rev_l, rev_r, d, u)] = t2i["R2_FX"]
    g_transform[Tile(key, rev_u, rev_d, r, l)] = t2i["R3"]
    g_transform[Tile(key, u, d, l, r)] = t2i["R3_FY"]
    g_transform[Tile(key, rev_d, rev_u, rev_r, rev_l)] = t2i["R3_FX"]

    return res


# Don't check, if it is == 0
# no_check_ids are the ones we already used
#@cached(cache=LRUCache(maxsize=100000), key=lambda tiles, r, d, no_check_ids: hashkey(r, d, no_check_ids))
def check_tiles(tiles, r, d, no_check_ids):
    for t in tiles:
        if t.id not in no_check_ids and (r == 0 or t.l == r) and (d == 0 or t.u == d):
            yield t


def find_combination(tiles, result_list, no_check_ids):

    if len(result_list) == tile_count:
        return result_list


    if len(result_list) == 0:
        r, d = 0, 0
    else:
        length = len(result_list)
        r = 0 if length % side_tile_count == 0 else result_list[-1].r
        d = 0 if length <= side_tile_count else result_list[-side_tile_count].d

    new_tiles = check_tiles(tiles, r, d, no_check_ids)

    for t in new_tiles:
        c = find_combination(tiles, result_list + [t], no_check_ids | {t.id})
        if c != []:
            return c

    # No valid combination found any more!
    return []


# Creates a proper 2d array and removes the sides and first/last row.
def to_2d_array(tile):
    ts = []
    for y in range(1, 10-1):
        tmp = tile[y*10 : (y+1)*10]
        ts.append("".join(tmp[1:-1]))
    return ts

# https://stackoverflow.com/questions/8421337/rotating-a-two-dimensional-array-in-python
def rot(tile):
    tile = list(zip(*tile[::-1]))
    return lmap(lambda x: "".join(x), tile)


def transform_tile(tiles, t):

    trans = i2t[g_transform[t]]
    rotate = int(trans[1])

    flip_y = "FY" in trans
    flip_x = "FX" in trans

    tile = tiles[t.id]
    tile = to_2d_array(tile)

    for i in range(rotate):
        tile = rot(tile)

    if flip_y:
        tile = tile[::-1]

    if flip_x:
        tile = lmap(lambda x: x[::-1], tile)

    return tile

# i are actual lines. So 8 per image.
def get_lines_at(tiles, i):

    offset_out = i//8
    offset_in  = i%8

    tile_row = tiles[offset_out*side_tile_count : (offset_out+1)*side_tile_count]

    return "".join(lmap(lambda x: x[offset_in], tile_row))


def combine_tiles(tiles):

    large_image = []

    for i in range(8*side_tile_count):
        large_image.append(get_lines_at(tiles, i))

    return large_image


def transform_monster():

    monster = ["..................#.", "#....##....##....###", ".#..#..#..#..#..#..."]
    monsters = []

    for i in range(4):

        new_monster = monster.copy()

        for i2 in range(i):
            new_monster = rot(new_monster)

        monsters.append(new_monster)
        monsters.append(new_monster[::-1])
        monsters.append(lmap(lambda x: x[::-1], new_monster))

    return monsters


def seek_and_destroy(img, monster, x, y, destroy=False):

    line_length = len(img[0])
    img_length  = len(img)

    for my, l in enumerate(monster):
        for mx, v in enumerate(l):
            if x+mx >= line_length:
                return False
            if y+my >= img_length:
                return False
            if v == "#" and img[y+my][x+mx] != "#":
                return False
            if destroy and v == "#":

                line = list(img[y+my])
                line[x+mx] = "."
                img[y+my] = "".join(line)

    return True


def seek_and_destroy_sea_monster(img):

    monsters = transform_monster()

    for y, l in enumerate(img):
        for x, _ in enumerate(l):
            for monster in monsters:
                if seek_and_destroy(img, monster, x, y):
                    seek_and_destroy(img, monster, x, y, destroy=True)


def main():

    images = open_data_groups("20.data")

    tiles = {int(i[0].split(" ")[1][:-1]): list("".join(i[1:])) for i in images}

    hashes = dict()
    # Precompute hashes for the sides
    for k, v in tiles.items():
        # key -> [possible_orientation]
        hashes[k] = all_combinations(
                        k,
                        get_l(v), get_r(v), get_u(v), get_d(v),
                        get_l(v, rev=True), get_r(v, rev=True), get_u(v, rev=True), get_d(v, rev=True)
        )

    # List of all possible tile orientations
    all_tiles = [t for ts in hashes.values() for t in ts]

    result = find_combination(all_tiles, [], set())
    print(result[0].id * result[side_tile_count-1].id * result[tile_count-side_tile_count].id * result[tile_count-1].id)


    result = lmap(lambda x: transform_tile(tiles, x), result)

    large_image = combine_tiles(result)

    seek_and_destroy_sea_monster(large_image)

    print(sum([v == "#" for l in large_image for v in l]))


if __name__ == "__main__":
    main()

# solution for 20.01: 140656720229539
# solution for 20.02: 1885
