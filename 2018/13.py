#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *

# \ corner
corner_map_1 = {(0,-1): (-1,0), (1,0): (0,1), (0,1): (1,0), (-1,0): (0,-1)}
# / corner
corner_map_2 = {(-1,0): (0,1), (0,-1): (1,0), (1,0): (0,-1), (0,1): (-1,0)}
# player dir map
dir_map = {"<": (-1,0), ">": (1,0), "^": (0,-1), "v": (0,1)}
rev_dir_map = {v:k for k,v in dir_map.items()}
# keep direction so we don't need any if-else and can just apply the direction update map
dir_map_normal = {k:k for k in [(0,-1), (-1,0), (1,0), (0,1)]}


def pp(field, carts):

    for y in range(7):
        for x in range(13):
            tmp = [x[0] for x in carts]
            if (x,y) in tmp:
                print(rev_dir_map[carts[tmp.index((x,y))][1]], end="")

            elif (x,y) not in field:
                print(" ", end="")
            else:
                print("+" if field[(x,y)][1] else ".", end="")
        print("")


# only works on sorted cart list
def find_collision(carts):
    for i, c1 in enumerate(carts):
        for j, c2 in enumerate(carts):
            if c1 != c2 and c1[0] == c2[0]:
                return c1, c2
    return None


def run(field, carts):
    print_first_part = True
    final_round = False

    while True:
        carts.sort(key=lambda x: (x[0][1], x[0][0]))

        # so we can savely iterate carts while removing from the list at the same time.
        # avoid index juggling at the cost of some performance.
        tmp = carts.copy()

        while len(tmp) > 0:
            c = tmp.pop(0)
            i = carts.index(c)

            # update position
            carts[i][0] = add(c[0], c[1])

            # cross road --> direction update
            if field[carts[i][0]][1]:
                # not straight ahead
                new_dir = c[1]
                if c[2] != 1:
                    new_dir = rotate(c[1], False, count=1 if c[2] == 0 else 3)
                carts[i][1] = new_dir
                carts[i][2] = (c[2]+1)%3
            else:
                carts[i][1] = field[carts[i][0]][0][c[1]]

            p = find_collision(carts)
            if p:
                if print_first_part:
                    print("{},{}".format(*p[0][0]))
                print_first_part = False

                carts.remove(p[0])
                carts.remove(p[1])
                if p[0] in tmp:
                    tmp.remove(p[0])
                if p[1] in tmp:
                    tmp.remove(p[1])

                if len(carts) == 1:
                    final_round = True

        if final_round:
            print("{},{}".format(*carts[0][0]))
            return


def main():

    lines = open_data("13.data")

    # (x,y) -> (corner-dict(), is_crossing)
    field = dict()
    # list of positions and current direction: [[(5,6), (1,0), cross_type: 0->left, 1->straight, 2->right]]
    carts = []

    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if c in "|-+v^<>" :
                field[(x,y)] = (dir_map_normal, c == "+")
                if c in "v^<>":
                    carts.append([(x,y), dir_map[c], 0])
            elif c == "\\":
                field[(x,y)] = (corner_map_1, False)
            elif c == "/":
                field[(x,y)] = (corner_map_2, False)

    run(field, carts)

if __name__ == "__main__":
    main()

# year 2018
# solution for 13.01: 83,49
# solution for 13.02: 73,36
