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

    jet_i = 0
    for i in range(2022):
        rock = rocks[i%len(rocks)]
        pos = (2, max(field.keys(), key=lambda x: x[1])[1]+len(rock)+3)

        for j in itertools.count():
            wind = jet[jet_i%len(jet)]
            pos = move_left_right(field, pos, rock, wind)
            jet_i += 1

            pos, rock_placed = move_down(field, pos, rock)

            if rock_placed:
                break

        place_rock(field, pos, rock)

    print(max(field.keys(), key=lambda x: x[1])[1])







if __name__ == "__main__":
    main()

# year 2022
# solution for 17.01: ?
# solution for 17.02: ?
