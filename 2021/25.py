#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def step(field, w, h):

    f1 = defaultdict(lambda: ".")
    done = True
    # right
    for (x,y) in list(field.keys()):
        if field[(x,y)] == ">":
            new_pos = ((x+1)%w, y)
            if field[new_pos] == ".":
                f1[new_pos] = ">"
                #field[(x,y)] = "."
                done = False
            else:
                f1[(x,y)] = ">"

    f2 = defaultdict(lambda: ".")
    # down
    for (x,y) in list(field.keys()):
        if field[(x,y)] == "v":
            new_pos = (x, (y+1)%h)
            if f1[new_pos] == "." and field[new_pos] != "v":
                f2[(x, (y+1)%h)] = "v"
                done = False
            else:
                f2[(x, y)] = "v"
        elif f1[(x,y)] == ">":
            f2[(x,y)] = ">"

    return f2, done

def main():

    lines = open_data("25.data")

    # 0 == nothing, 1 == down, 2 == right
    field = defaultdict(lambda: ".")
    for y, l in enumerate(lines):
        for x,c in enumerate(l):
            field[(x,y)] = c
    w, h = len(lines[0]), len(lines)

    #draw(field, symbols={-1:".", ".":".", "v":"v", ">":">"})


    for i in itertools.count():
    #for i in range(10):
        field, done = step(field.copy(), w, h)
        #print("Step {}:".format(i+1))
        #draw(field, symbols={-1:".", ".":".", "v":"v", ">":">"})
        #break

        #if i == 3:
        #    draw(field, symbols={-1:".", ".":".", "v":"v", ">":">"})

        if done:
            print(i+1)
            break

    #draw(field, symbols={-1:".", ".":".", "v":"v", ">":">"})




if __name__ == "__main__":
    main()

# year 2021
# solution for 25.01: ?
# solution for 25.02: ?
