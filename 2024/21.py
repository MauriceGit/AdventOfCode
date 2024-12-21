#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

d_to_c = {(-1,0):"<", (1,0):">", (0,-1):"^", (0,1):"v", (0,0):"A"}
c_to_d = {v:k for k,v in d_to_c.items()}

def check_path(pos, path, forbidden):
    for p in path:
        pos = add(pos, c_to_d[p])
        if pos == forbidden:
            return False
    return True

def all_numpad_paths(code):
    pad = {(0,0):"7",(1,0):"8",(2,0):"9", (0,1):"4",(1,1):"5",(2,1):"6", (0,2):"1",(1,2):"2",(2,2):"3", (1,3):"0",(2,3):"A"}
    rev_pad = {v:k for k,v in pad.items()}

    paths = set([""])
    pos = (2,3)
    for c in code:

        diff = sub(rev_pad[c], pos)
        dx = ("<" if diff[0] < 0 else ">") * abs(diff[0])
        dy = ("^" if diff[1] < 0 else "v") * abs(diff[1])

        new_paths_1 = set()
        new_paths_2 = set()
        if check_path(pos, dx+dy, (0,3)):
            new_paths_1 = {p+dx+dy+"A" for p in paths}
        if check_path(pos, dy+dx, (0,3)):
            new_paths_2 = {p+dy+dx+"A" for p in paths}

        paths = new_paths_1 | new_paths_2

        pos = rev_pad[c]
    return paths


def all_dirpad_paths(code):
    pad = {(1,0):"^", (2,0):"A", (0,1):"<", (1,1):"v", (2,1):">"}
    rev_pad = {v:k for k,v in pad.items()}

    pos = (2,0)
    paths = set([""])
    for c in code:

        diff = sub(rev_pad[c], pos)
        dx = ("<" if diff[0] < 0 else ">") * abs(diff[0])
        dy = ("^" if diff[1] < 0 else "v") * abs(diff[1])
        new_paths_1 = set()
        new_paths_2 = set()
        if check_path(pos, dx+dy, (0,0)):
            new_paths_1 = {p+dx+dy+"A" for p in paths}
        if check_path(pos, dy+dx, (0,0)):
            new_paths_2 = {p+dy+dx+"A" for p in paths}

        paths = new_paths_1 | new_paths_2

        pos = rev_pad[c]
    return paths


def all_paths(paths):
    out = []
    for p in paths:
        out.extend(all_dirpad_paths(p))
    return out

def rec_all_paths(paths, rec):
    if rec == 0:
        return paths
    return rec_all_paths(all_paths(paths), rec-1)

def main():

    codes = open_data("21.data")
    #c = codes[:1][0]

    #for c in codes:
    #    print(all_numpad_paths(c))
    #
    #
    #return

    complexity = 0
    for c in codes:
        #print(lmap(len, all_paths(all_paths(all_numpad_paths(c)))))
        tmp = all_paths(all_paths(all_paths(all_numpad_paths(c)))[:1])
        print(tmp[0])
        complexity += int(c[:-1]) * min(map(len, tmp))
        #complexity += int(c[:-1]) * min(map(len, rec_all_paths(all_numpad_paths(c), 3)))
    print(complexity)





if __name__ == "__main__":
    main()

# year 2024
# solution for 21.01: ?
# solution for 21.02: ?
