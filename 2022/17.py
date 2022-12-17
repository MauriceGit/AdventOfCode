#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

# return (new_pos, hit_bottom)
def check_pos(field, pos, rock, offset):
    new_pos = add(pos, offset)

    if new_pos[0] < 0 or new_pos[0]+len(rock[0]) > 7:
        return pos, False

    for y, row in enumerate(rock):
        for x, c in enumerate(row):
            if c == "#" and add(new_pos, (x,-y)) in field:
                return pos, True

    return new_pos, False


# returns updated rock position
def move_left_right(field, pos, rock, wind):
    return check_pos(field, pos, rock, (-1,0) if wind == "<" else (1,0))[0]

# return (new_pos, hit_bottom)
def move_down(field, pos, rock):
    return check_pos(field, pos, rock, (0,-1))

def place_rock(field, pos, rock):
    for y, row in enumerate(rock):
        for x, c in enumerate(row):
            if c == "#":
                field[add(pos, (x,-y))] = "#"

def run(field, jet, rocks, iterations):
    jet_i = 0
    for i in range(iterations):
        rock = rocks[i%len(rocks)]
        pos = (2, max(field.keys(), key=lambda x: x[1])[1]+len(rock)+3)

        for j in itertools.count():
            wind = jet[jet_i%len(jet)]
            pos = move_left_right(field, pos, rock, wind)
            jet_i += 1

            pos, rock_placed = move_down(field, pos, rock)

            if rock_placed:
                # print jet_i%len(jet) here for analysis when everything repeats!
                break

        place_rock(field, pos, rock)

    return max(field.keys(), key=lambda x: x[1])[1]

def main():

    jet = open_data("17.data")[0]

    rocks = [
        ["####"],
        [".#.", "###", ".#."],
        ["..#", "..#", "###"],
        ["#", "#", "#", "#"],
        ["##", "##"]
    ]

    field = dict()
    for i in range(7):
        field[(i,0)] = "#"

    print(run(field.copy(), jet, rocks, 2022))

    # Initial offset is 800 repetitions (probably fewer but who cares).
    # Then 1700 jet (input) indices repeat forever! (counted when a rock is finally placed!)
    # The initial height at 800 repetitions is: 1230
    # Then the height after each group is: 1230, 3884, 6538
    # So the height grows 2654 each iteration
    #
    # That means, after subtracting 800 rounds, we have 999999999200 rounds remaining.
    # So dividing this by 1700, we have 588235293 full block repetitions (*2654 height)
    # After that, in the end, we have 1100 rounds remaining (999999999200%1700).
    #
    # The initial 800 rounds + 1100 rounds remaining create a tower of height: 2947
    #
    # So 588235293*2654 + 2947 == 1561176470569

    print(588235293*2654 + run(field.copy(), jet, rocks, 800+1100))


if __name__ == "__main__":
    main()

# year 2022
# solution for 17.01: 3124
# solution for 17.02: 1561176470569
