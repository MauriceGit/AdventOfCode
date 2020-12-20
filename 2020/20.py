#!/usr/bin/env python3.7

from utility import *

Tile = namedtuple("Tile", "id l r u d")

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

    return list({
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



# Don't check, if it is == 0
# no_check_ids are the ones we already used
#@cached(cache=LRUCache(maxsize=100000), key=lambda tiles, r, d, no_check_ids: hashkey(r, d, no_check_ids))
def check_tiles(tiles, r, d, no_check_ids):

    res = []
    for t in tiles:
        if t.id not in no_check_ids:
            if (r == 0 or t.l == r) and (d == 0 or t.u == d):
                res.append(t)
    return res


# TODO: change to 144 and 12
tile_count = 144
side_tile_count = 12

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



    #for r in result:
    #    print(r.id, end=" ")
    #print()

    #print(result[0].id, result[side_tile_count-1].id, result[tile_count-side_tile_count].id, result[tile_count-1].id)

    print(result[0].id * result[side_tile_count-1].id * result[tile_count-side_tile_count].id * result[tile_count-1].id)





if __name__ == "__main__":
    main()

# solution for 20.01: ?
# solution for 20.02: ?
