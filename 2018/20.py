#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


dir_map = dict(zip("EWSN", dir_list_4()))

def find_closing_bracket(s):
    count = 0
    for i,c in enumerate(s):
        count += c == "("
        count -= c == ")"
        if count == -1:
            return i
    return 0


def parse_tree(field, string, pos=(0,0)):

    # Save the position at the very beginning of the function!
    # Go the next direction in the path, until a '(' is found.
    # then recurse with the string from the beginning until the last ')'
    # When encountering a '|', go back to the save-position from the
    # beginning and start again with the next part.
    #
    # This should be able to parse the whole tree without overhead!

    start_pos = pos
    i = 0
    while i < len(string):
        c = string[i]
        if c in "NSEW":
            door = add(pos, dir_map[c])
            pos  = add(door, dir_map[c])
            field[pos] = 1
            field[door] = 2
        if c == "|":
            pos = start_pos
        if c == "(":
            last_index = i+1+find_closing_bracket(string[i+1:])
            parse_tree(field, string[i+1:last_index], pos=pos)
            i = last_index
        i += 1


def bfs(field, pos):

    visited = set()
    queue = [(pos, 0)]
    distances = []

    while len(queue) > 0:
        p, dist = queue.pop(0)

        if p in visited:
            continue

        visited.add(p)
        distances.append((p, dist))

        for d in dir_list_4():
            door = add(p, d)
            new_p = add(door, d)
            if field[new_p] != 0 and field[door] != 0 and new_p not in visited:
                queue.append((new_p, dist+1))

    return distances


def main():

    line = open_data("20.data")[0]

    field = defaultdict(int)
    parse_tree(field, line[1:-1])

    distances = bfs(field, (0,0))
    distances.sort(key=lambda x: x[1])

    print(distances[-1])
    print(len(lfilter(lambda x: x[1] >= 1000, distances)))

    #draw(field, print_directly=True)


if __name__ == "__main__":
    main()

# year 2018
# solution for 20.01: 3725
# solution for 20.02: 8541
