#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def main():

    lines = open_data("10.data")

    queue = []
    bots = defaultdict(list)
    # ((to_output, INT), (to_output, INT))
    instructions = defaultdict(tuple)
    bins = defaultdict(list)

    responsible = -1

    for l in lines:
        if l.startswith("value"):
            value, bot = ints(l)
            bots[bot].append(value)
            queue.append(bot)
        else:
            bot, low, high = ints(l)
            a, b = l.split("and")
            instructions[bot] = (("output" in a, low), ("output" in b, high))

    while len(queue) > 0:
        bot = queue.pop()
        if len(bots[bot]) < 2:
            continue
        (low_out, low), (high_out, high) = instructions[bot]

        if 61 in bots[bot] and 17 in bots[bot]:
            responsible = bot

        (bins if low_out else bots)[low].append(min(bots[bot]))
        (bins if high_out else bots)[high].append(max(bots[bot]))

        queue.append(low)
        queue.append(high)

        bots[bot] = []

    print(responsible)
    print(bins[0][0]*bins[1][0]*bins[2][0])


if __name__ == "__main__":
    main()

# year 2016
# solution for 10.01: 113
# solution for 10.02: 12803
