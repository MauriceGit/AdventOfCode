#!/usr/bin/env python3.7

from operator import itemgetter

def eval_lines(lines):
    lines = list(map(lambda x: int(x.split(" ")[3].split("ms")[0]), lines))
    return round(sum(lines)/len(lines)), min(lines), max(lines)


def main():

    lines = open("all_solutions.txt", "r").read().splitlines()

    parts = [[l for i,l in enumerate(lines) if i%2 == 0], [l for i,l in enumerate(lines) if i%2 == 1]]

    print("Solutions evaluated: {}".format(len(lines)))

    runtimes = list(map(eval_lines, parts))
    for i,p in enumerate(runtimes):
        print("Day 23 part {} runtime  -- avg: {}ms, min: {}ms, max: {}ms".format(i+1, *p))

    avgs = list(map(itemgetter(0), runtimes))
    mins = list(map(itemgetter(1), runtimes))
    maxs = list(map(itemgetter(2), runtimes))
    print("Day 23 overall runtime -- avg: {}ms, min: {}ms, max: {}ms".format(sum(avgs)//len(avgs), min(mins), max(maxs)))


if __name__ == "__main__":
    main()
