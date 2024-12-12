#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

# trace AROUND the shape. Starting in the upper left corner.
def trace_outline(plot, fence_positions, p_start):
    d = (1, 0)
    p = p_start

    while add(p, rotate(d, True)) not in plot:
        d = rotate(d, True)

    if all(add(p, d) in plot for d in dir_list_4()):
        return 4, {p}

    fences = 0
    finished_fences = {p}
    d_start = d

    while p != p_start or d != d_start or fences == 0:

        if add(p, d) not in plot:
            finished_fences.add(p)
            p = add(p, d)

        # if there is no block right of my movement direction, we turn right!
        if add(p, rotate(d, True)) not in plot:
            d = rotate(d, True)
            fences += 1

        # if we would move into ourself, we turn left!
        while add(p, d) in plot:
            d = rotate(d, False)
            fences += 1

    return fences, finished_fences


def main():

    lines = open_data("12.data")

    f = dict()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            f[(x,y)] = c

    # list of plots [[(x,y)], ...]
    plots = []

    while len(f) > 0:
        start = next(iter(f.keys()))
        plot_type = f[start]
        plot = set()
        def get_neighbors(state, pos):
            for d in dir_list_4():
                n = add(pos, d)
                if n in f and f[n] == plot_type:
                    yield add(pos, d)
        def visit(state, pos, dist, path):
            plot.add(pos)
            del f[pos]
            return True

        dijkstra(start, get_neighbors, visit=visit)
        plots.append(plot)

    part1 = 0
    part2 = 0
    for i, plot in enumerate(plots):
        fence_positions = set()
        fences = 0
        for p in plot:
            for d in dir_list_4():
                fences += add(p, d) not in plot
                if add(p, d) not in plot:
                    fence_positions.add(add(p, d))
        part1 += len(plot) * fences

        fences = 0
        while len(fence_positions) > 0:
            _fence, finished_fences = trace_outline(plot, fence_positions, min(fence_positions, key=itemgetter(1, 0)))
            fence_positions = fence_positions - finished_fences
            fences += _fence
        part2 += len(plot) * fences

    print(part1)
    print(part2)


if __name__ == "__main__":
    main()

# year 2024
# solution for 12.01: 1370258
# solution for 12.02: 805814
