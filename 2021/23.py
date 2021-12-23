#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def pp(occupied, final_pos, hallway):
    field = dict()
    for x in range(-1, 12):
        for y in range(-1, 6):
            field[(x,y)] = "#"
    for x in range(10):
        field[(x, 0)] = "."
    for hw in hallway:
        field[hw] = "."
    for ps in final_pos.values():
        for p in ps:
            field[p] = "."
    for p, t in occupied.items():
        if occupied[p] != "":
            field[p] = t
    draw(field, print_directly=True)


def horizontal(p0, p1):
    positions = []
    x,y = p0
    while x != p1[0]:
        x += 1 if p1[0] > x else -1
        positions.append((x,y))
    return positions


def vertical(p0, p1):
    positions = []
    x, y = p0
    while y > 0:
        y -= 1
        positions.append((x,y))
    return positions


def all_steps_unoccupied(occupied, amph_type, p0, p1):

    if p0[1] > 0:
        positions = vertical(p0, p1)
        positions += horizontal(positions[-1], p1)
    else:
        positions = horizontal(p0, p1)
        positions += vertical(positions[-1], p1)

    for p in positions:
        if occupied[p] != "":
            return False
    return True


def anything_clear_below(final_positions, occupied, p1):
    for p in final_positions:
        if p[1] > p1[1] and occupied[p] == "":
            return True
    return False


def path_clear(occupied, final_pos, amph_type, p0, p1):

    # stays in hallway
    # tries to skip hallway
    if (p0[1] > 0) == (p1[1] > 0):
        return False

    # tries wrong room
    if p1[1] > 0 and p1 not in final_pos[amph_type]:
        return False

    final_positions = final_pos[amph_type]
    ok = all([occupied[p] in ["", amph_type] for p in final_positions])
    if p1[1] > 0 and not ok:
        return False

    # tries to stop at the upper-most position
    if p1[1] > 0 and anything_clear_below(final_positions, occupied, p1):
        return False

    # room to hallway
    return all_steps_unoccupied(occupied, amph_type, p0, p1)


def get_all_moves(amphipods, occupied, final_pos, hallway, energie, steps):
    all_moves = []
    for amph_type, amph_l in amphipods.items():
        for amph in amph_l:
            for hp in hallway:
                ok = path_clear(occupied, final_pos, amph_type, amph, hp)
                if ok:
                    all_moves.append((steps[(amph, hp)]*energie[amph_type], amph_type, amph, hp))
            for fp in final_pos[amph_type]:
                if path_clear(occupied, final_pos, amph_type, amph, fp):
                    all_moves.append((steps[(amph, fp)]*energie[amph_type], amph_type, amph, fp))
    return all_moves


def all_final(amphipods, final_pos):
    for amph_type, amph_l in amphipods.items():
        for amph in amph_l:
            if amph not in final_pos[amph_type]:
                return False
    return True


def make_move(occupied, amphipods, t, pfrom, pto):
    occupied[pfrom] = ""
    occupied[pto] = t
    amphipods[t] = (amphipods[t] - set([pfrom])) | set([pto])


def move(total_energie, path, _amphipods, _occupied, final_pos, hallway, energie, steps, level=0):

    # make a list of all possible moves room --> hallway and hallway --> final_room.
    moves = get_all_moves(_amphipods, _occupied, final_pos, hallway, energie, steps)

    # [(used_energie, path)]
    queue = [(0, [])]
    heapify(queue)

    visited = set()

    while len(queue) > 0:

        occ = _occupied.copy()
        amphs = _amphipods.copy()

        used_energie, path = heappop(queue)

        for m in path:
            make_move(occ, amphs, m[1], m[2], m[3])

        # check, if we're done!
        if all_final(amphs, final_pos):
            return used_energie

        key = tuple(occ.items())
        if key in visited:
            continue
        visited.add(key)

        new_moves = get_all_moves(amphs, occ, final_pos, hallway, energie, steps)
        for m in new_moves:
            heappush(queue, (used_energie+m[0], path + [m]))

    return 100000000, []


def doyourthing(amphipods, final_pos):

    hallway = [(0,0), (1,0), (3,0), (5,0), (7,0), (9,0), (10,0)]
    occupied = defaultdict(lambda: "")
    energie = {"A": 1, "B": 10, "C": 100, "D": 1000}

    for t, ps in amphipods.items():
        for p in ps:
            occupied[p] = t

    #pp(occupied, final_pos, hallway)

    steps = dict()
    for hp in hallway:
        for ps in final_pos.values():
            for p in ps:
                steps[(p, hp)] = manhatten_dist(p, hp)
                steps[(hp, p)] = manhatten_dist(p, hp)

    return move(0, [], amphipods, occupied, final_pos, hallway, energie, steps)


def main():

    groups = open_data_groups("23.data")

    for start_field in groups:

        amphipods = defaultdict(set)
        for y,l in enumerate(start_field):
            for x,c in enumerate(l):
                if c in "ABCD":
                    amphipods[c].add((x-1, y-1))

        final_pos = {
            "A": [(2, y+1) for y in range(len(start_field)-3)],
            "B": [(4, y+1) for y in range(len(start_field)-3)],
            "C": [(6, y+1) for y in range(len(start_field)-3)],
            "D": [(8, y+1) for y in range(len(start_field)-3)]
        }

        print(doyourthing(amphipods, final_pos))


if __name__ == "__main__":
    main()

# year 2021
# solution for 23.01: 14510
# solution for 23.02: 49180
