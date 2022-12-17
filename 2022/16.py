#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

Valve = recordtype("Valve", "flow_rate is_open tunnels")
State = recordtype("State", "score open_valves v minutes history")


cache = dict()
def try_valve2(valves, open_valves, current, minutes, score, history):

    if minutes >= 30:
        return score, history

    key = (score, current, minutes)
    if key in cache:
        return cache[key]

    best = (score, history)
    for open_valve in [True, False]:
        tmp_history = history
        tmp_open_valves = open_valves
        tmp_minutes = minutes
        tmp_score = score

        ok = not open_valve
        if open_valve and valves[current].flow_rate > 0 and f"[{current}]" not in tmp_open_valves:
            tmp_history += f" [{current}]"
            tmp_open_valves += f"[{current}]"
            tmp_minutes += 1
            tmp_score += (30-tmp_minutes) * valves[current].flow_rate
            ok = True

        if ok:
            for new_valve in valves[current].tunnels:
                s, p = try_valve2(valves, tmp_open_valves, new_valve, tmp_minutes+1, tmp_score, tmp_history+f" -> {new_valve}")
                if s > best[0]:
                    best = (s, p)

    cache[key] = best
    return best



def main():

    lines = open_data("16.data")

    valves = dict()

    for line in lines:
        l = line.split(" ")
        v = l[1]
        flow_rate = ints(line)[0]
        vs = line.split(" to ")[1].replace(",", "").split(" ")[1:]
        valves[v] = Valve(flow_rate, False, vs)


    print(try_valve2(valves, "", "AA", 0, 0, "AA"))


if __name__ == "__main__":
    main()

# year 2022
# solution for 16.01: 2265
# solution for 16.02: ?
