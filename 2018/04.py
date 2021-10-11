#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *

def add_times(l, start, end):
    l2 = [0 if i < start or i > end else 1 for i in range(60)]
    lout = list(map(sum, zip(l, l2)))
    print(start, end, l2)
    return lout


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
            print("guard: ", current_guard)
            guards[current_guard] = add_times(guards[current_guard], sleep_time, int(s[1][3:5]))

    #print(guards)
    for g in guards.items():
        print(g)

    guard_id = max(guards.items(), key=lambda x: sum(x[1]))
    minute = max(guards[guard_id[0]])
    print(guard_id[0], guard_id[1].index(minute))
    print(guard_id[0] * guard_id[1].index(minute))



    # > 7233

if __name__ == "__main__":
    main()

# year 2018
# solution for 04.01: 101262
# solution for 04.02: ?
