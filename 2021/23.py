#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


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


def path_clear(occupied, final_pos, amph_type, p0, p1):

    if p0 in final_pos[amph_type]:
        return False

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

    # hallway to room
    if p1[1] == 1 and occupied[(p1[0],2)] == "":
        # stops at first room pos but second one is empty as well!
        return False

    # room to hallway
    return all_steps_unoccupied(occupied, amph_type, p0, p1)


# make generator!
def get_all_moves(amphipods, occupied, final_pos, hallway, energie, steps):
    all_moves = []
    for amph_type, amph_l in amphipods.items():
        for amph in amph_l:
            for hp in hallway:
                ok = path_clear(occupied, final_pos, amph_type, amph, hp)
                #print("{} -> {}: {}", amph, hp)
                if ok:
                    #yield (steps[(amph, hp)]*energie[amph_type], amph_type, amph, hp)
                    all_moves.append((steps[(amph, hp)]*energie[amph_type], amph_type, amph, hp))
            for fp in final_pos[amph_type]:
                if path_clear(occupied, final_pos, amph_type, amph, fp):
                    #yield (steps[(amph, fp)]*energie[amph_type], amph_type, amph, fp)
                    #print()
                    all_moves.append((steps[(amph, fp)]*energie[amph_type], amph_type, amph, fp))
    return all_moves

def all_final(amphipods, final_pos):
    for amph_type, amph_l in amphipods.items():
        for amph in amph_l:
            if amph not in final_pos[amph_type]:
                return False
    return True


cache = dict()

def move(total_energie, path, amphipods, occupied, final_pos, hallway, energie, steps, level=0):

    # check, if we're done!
    if all_final(amphipods, final_pos):
        return total_energie, path

    cache_key = (tuple(occupied.items()))
    posses = amphipods.items()
    posses = [(t, tuple(sorted(list(ps)))) for t, ps in posses]
    cache_key = tuple(posses)
    if cache_key in cache:
        return cache[cache_key]

    # make a list of all possible moves room --> hallway and hallway --> final_room.
    queue = get_all_moves(amphipods, occupied, final_pos, hallway, energie, steps)
    #all_moves.sort()

    #print(len(all_moves), level, total_energie)

    #pp(occupied, final_pos, hallway)

    energies = []

    for m in queue:
        #print("try:", m)

        e, t, pfrom, pto = m

        tmp_occ = occupied.copy()
        tmp_occ[pfrom] = ""
        tmp_occ[pto] = t

        tmp_amphs = amphipods.copy()
        tmp_amphs[t] = (tmp_amphs[t] - set([pfrom])) | set([pto])

        tmp_energie, tmp_path = move(total_energie + e, path + [m], tmp_amphs, tmp_occ, final_pos, hallway, energie, steps, level=level+1)

        #if level == 0:
        #    print(tmp_energie)

        energies.append((tmp_energie, tmp_path))

    if len(energies) == 0:
        return 1000000000, []

    res = min(energies, key=lambda x: x[0])

    cache[cache_key] = res

    return res




def pp(occupied, final_pos, hallway):

    field = dict()

    for x in range(-1, 12):
        for y in range(-1, 4):
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


def make_move(occupied, amphipods, t, pfrom, pto):
    occupied[pfrom] = ""
    occupied[pto] = t
    amphipods[t] = (amphipods[t] - set([pfrom])) | set([pto])

def main():

    lines = open_data("23.data")

    #############
    #...........#
    ###B#A#B#C###
      #C#D#D#A#
      #########

    # There are only exactly of two steps for each amphipod:
    #   pos --> hallway --> final_pos


    hallway = [(0,0), (1,0), (3,0), (5,0), (7,0), (9,0), (10,0)]
    amphipods = {"A": {(4,1), (8,2)}, "B": {(2,1), (6,1)}, "C": {(2,2), (8,1)}, "D": {(4,2), (6,2)}}
    #amphipods = {"A": {(4,2)}, "B": {(2,2)}}
    final_pos = {"A": [(2,2), (2,1)], "B": [(4,2), (4,1)], "C": [(6,2), (6,1)], "D": [(8,2), (8,1)]}
    #final_pos = {"A": [(2,2), (2,1)], "B": [(4,2), (4,1)]}
    # pos --> "A"
    occupied = defaultdict(lambda: "")
    energie = {"A": 1, "B": 10, "C": 100, "D": 1000}



    for t, ps in amphipods.items():
        for p in ps:
            occupied[p] = t

    pp(occupied, final_pos, hallway)
    #return

    steps = dict()
    for hp in hallway:
        for ps in final_pos.values():
            for p in ps:
                steps[(p, hp)] = manhatten_dist(p, hp)
                steps[(hp, p)] = manhatten_dist(p, hp)



    score, moves = move(0, [], amphipods, occupied, final_pos, hallway, energie, steps)


    for m in moves:
        e, t, pfrom, pto = m
        make_move(occupied, amphipods, t, pfrom, pto)
        pp(occupied, final_pos, hallway)
    print(score)


if __name__ == "__main__":
    main()

# year 2021
# solution for 23.01: ?
# solution for 23.02: ?
