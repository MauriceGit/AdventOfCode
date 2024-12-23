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


@lru_cache(maxsize=100)
def dirs(seq):
    pad = {(1,0):"^", (2,0):"A", (0,1):"<", (1,1):"v", (2,1):">"}
    rev_pad = {v:k for k,v in pad.items()}

    all_out = [""]

    pos = (2,0)
    for c in seq:
        diff = sub(rev_pad[c], pos)
        dx = ("<" if diff[0] < 0 else ">") * abs(diff[0])
        dy = ("^" if diff[1] < 0 else "v") * abs(diff[1])
        p1 = ""
        p2 = ""
        if check_path(pos, dx+dy, (0,0)):
            p1 = dx+dy+"A"
        if check_path(pos, dy+dx, (0,0)):
            p2 = dy+dx+"A"

        if diff != (0, 0):
            _out1, _out2 = [], []
            if p1 != "":
                _out1 = [p+p1 for p in all_out]
            if p2 != "":
                _out2 = [p+p2 for p in all_out]
            all_out = _out1 + _out2
        else:
            all_out = [p+"A" for p in all_out]

        pos = rev_pad[c]

    return lmap(lambda x: lmap(lambda y: y+"A", x), map(lambda x: x.split("A")[:-1], all_out))

@lru_cache(maxsize=10000000000)
def solve_seq(seq, req):
    if req == 0:
        return len(seq)

    possible_next_sequences = dirs(seq)
    best_sequence = 100000000000000000000000
    for next_seq in possible_next_sequences:
        count = sum(solve_seq(n, req-1) for n in next_seq)
        best_sequence = min(best_sequence, count)

    return best_sequence


# sequence: [str]
def solve(sequence):
    return sum(solve_seq(seq, 25) for seq in sequence)


def main():

    codes = open_data("21.data")

    sum_all = 0
    for c in codes:
        tmp = lmap(lambda x: lmap(lambda y: y+"A", x), map(lambda x: x.split("A")[:-1], all_numpad_paths(c)))
        s = min(solve(sequence) for sequence in tmp)
        sum_all += s * int(c[:-1])
    print(sum_all)


if __name__ == "__main__":
    main()

# year 2024
# solution for 21.01: 138764
# solution for 21.02: 169137886514152
