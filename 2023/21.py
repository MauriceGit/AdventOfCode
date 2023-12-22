#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

def calc_step_area_complete(start_pos, f, f_count, w, h, max_step_count):
    State = recordtype("State", "field count")

    def get_neighbors(state, pos):
        for d in dir_list_4():
            pos2 = add(pos, d)
            pos2 = (pos2[0]%w, pos2[1]%h)
            if state.field[pos2] != "#":
                yield add(pos, d)

    def visit(state, pos, dist, path):
        if dist%2 == max_step_count%2:
            pos2 = (pos[0]%w, pos[1]%h)
            state.count[pos2] += 1
        return dist <= max_step_count

    state = State(f, f_count)
    dijkstra(start_pos, get_neighbors, state=state, visit=visit)
    return sum(f_count.values())

def calc_step_area(start_pos, f, f_count, w, h, max_step_count, even=True):
    State = recordtype("State", "field count")

    def get_neighbors(state, pos):
        for d in dir_list_4():
            if add(pos,d) in state.field and state.field[add(pos,d)] != "#":
                yield add(pos,d)

    def visit(state, pos, dist, path):
        if dist%2 == (0 if even else 1):
            state.count[pos] = 1
        return dist <= max_step_count


    state = State(f, f_count)
    if type(start_pos) == list:
        for pos in start_pos:
            dijkstra(pos, get_neighbors, state=state, visit=visit)
    else:
        dijkstra(start_pos, get_neighbors, state=state, visit=visit)
    return sum(f_count.values())


def main():

    lines = open_data("21.data")

    # (x,y, steps)
    pos = (0,0)
    f = dict()
    f_count = dict()
    for y,line in enumerate(lines):
        for x,c in enumerate(line):
            if c in "S":
                pos = (x,y)
            f[(x,y)] = c if c in ".#" else "."
            f_count[(x,y)] = 0

    w = len(lines[0])
    h = len(lines)

    print(calc_step_area_complete(pos, f, f_count.copy(), w, h, 64))

    original_steps = 26501365
    length = w

    def calc_area(start, count, even):
        return calc_step_area(start, f, f_count.copy(), w, h, count, even=even)

    steps = original_steps - (length//2)
    # The field count also starts with 'odd'
    odd  = calc_step_area(pos, f, f_count.copy(), w, h, 10000000000, even=False)
    even = calc_step_area(pos, f, f_count.copy(), w, h, 10000000000, even=True)

    field_cycles = steps//length
    remaining_steps = steps%length

    start_even = original_steps%2 == 0
    def base_coverage(step):
        count = odd
        while step > 0:
            count += step*4*(even if step%2 != start_even else odd)
            step -= 1
        return count

    base_count = base_coverage(field_cycles)
    # If the LAST field cycle is even
    is_even = field_cycles%2 != 0

    just_outside = 0
    # bottom left
    just_outside += calc_area((0,h-1), (length//2)-1, not is_even)
    # bottom right
    just_outside += calc_area((w-1,h-1), (length//2)-1, not is_even)
    # top right
    just_outside += calc_area((w-1,0), (length//2)-1, not is_even)
    # top left
    just_outside += calc_area((0,0), (length//2)-1, not is_even)
    just_outside *= field_cycles

    # subtract non-filled parts of the outer head fields
    head_subtract = 0
    sub = odd
    # top
    head_subtract += sub - calc_area((w//2,h-1), length-1, not is_even)
    # bottom
    head_subtract += sub - calc_area((w//2,0), length-1, not is_even)
    # right
    head_subtract += sub - calc_area((0,h//2), length-1, not is_even)
    # left
    head_subtract += sub - calc_area((w-1,h//2), length-1, not is_even)

    # subtract non-filled parts of the outer corner fields
    corner_subtract = 0
    sub = even if is_even else odd
    # bottom left
    corner_subtract += sub - calc_area([(0,h//2), (w//2,h-1)], length-1, not is_even)

    # bottom right
    corner_subtract += sub - calc_area([(w-1,h//2), (w//2,h-1)], length-1, not is_even)
    # top right
    corner_subtract += sub - calc_area([(w-1,h//2), (w//2,0)], length-1, not is_even)
    # top left
    corner_subtract += sub - calc_area([(0,h//2), (w//2,0)], length-1, not is_even)
    corner_subtract *= field_cycles-1

    print(base_count + just_outside - head_subtract - corner_subtract)


if __name__ == "__main__":
    main()

# year 2023
# solution for 21.01: 3820
# solution for 21.02: 632421652138917
