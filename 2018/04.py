#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *

def add_times(l, start, end):
    l2 = [i >= start and i < end for i in range(60)]
    return lmap(sum, zip(l, l2))


def main():

    lines = open_data("04.data")
    lines = sorted(lines, key=lambda k: k.split("]")[0])

    guards = defaultdict(lambda: [0]*60)

    current_guard = ""
    sleep_time = 0
    for l in lines:
        s = l.split(" ")
        if s[2] == "Guard":
            current_guard = int(s[3][1:])
        if s[2] == "falls":
            sleep_time = int(s[1][3:5])
        if s[2] == "wakes":
            guards[current_guard] = add_times(guards[current_guard], sleep_time, int(s[1][3:5]))

    guard_id = max(guards.items(), key=lambda x: sum(x[1]))
    minute = max(guards[guard_id[0]])
    print(guard_id[0] * guard_id[1].index(minute))

    guard_id = max(guards.items(), key=lambda x: max(x[1]))
    minute = max(guards[guard_id[0]])
    print(guard_id[0] * guard_id[1].index(minute))


if __name__ == "__main__":
    main()

# year 2018
# solution for 04.01: 101262
# solution for 04.02: 71976
