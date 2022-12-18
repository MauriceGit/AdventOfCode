#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

Valve = recordtype("Valve", "flow_rate tunnels")
State = recordtype("State", "score open_valves v minutes history")


#cache = dict()
#def try_valve(valves, open_valves, current, minutes, score):
#
#    if minutes >= 30:
#        return score
#
#    key = (score, current, minutes)
#    if key in cache:
#        return cache[key]
#
#    best = score
#    for open_valve in [True, False]:
#        tmp_open_valves = open_valves
#        tmp_minutes = minutes
#        tmp_score = score
#
#        ok = not open_valve
#        if open_valve and valves[current].flow_rate > 0 and f"[{current}]" not in tmp_open_valves:
#            tmp_open_valves += f"[{current}]"
#            tmp_minutes += 1
#            tmp_score += (30-tmp_minutes) * valves[current].flow_rate
#            ok = True
#
#        if ok:
#            for new_valve in valves[current].tunnels:
#                best = max(best, try_valve(valves, tmp_open_valves, new_valve, tmp_minutes+1, tmp_score))
#
#    cache[key] = best
#    return best


#best_score_yet = 0
cache = dict()
def try_valve2(valves, id_to_int, tunnel_cost, open_valves, current, minutes, score):

    if minutes[0] >= 26 and minutes[1] > 26:
        return score

    c0 = current[0]
    c1 = current[1]
    m0 = minutes[0]
    m1 = minutes[1]

    c = id_to_int[c0]<<6|id_to_int[c1] if c0 < c1 else id_to_int[c1]<<6|id_to_int[c0]
    m = m0<<5|m1 if m0 < m1 else m1<<5|m0
    # c: 12bit, m: 10bit, score: 12bit (max 4096)
    key = score<<22 | c<<10 | m
    if key in cache:
        return cache[key]

    best = score
    for i, candidate in enumerate(current):
        if minutes[i] >= 26:
            continue
        for open_valve in [True, False]:
            tmp_open_valves = open_valves
            tmp_minutes = minutes.copy()
            tmp_score = score

            ok = not open_valve
            # only the first candidate tries to open the valve, if both are on the same spot.
            not_same = current[0] != current[1] or i == 0
            if open_valve and valves[candidate].flow_rate > 0 and f"[{candidate}]" not in tmp_open_valves and not_same:
                tmp_open_valves += f"[{candidate}]"
                tmp_minutes[i] += 1
                tmp_score += (26-tmp_minutes[i]) * valves[candidate].flow_rate
                ok = True

            if ok:
                for new_valve in valves[candidate].tunnels:
                    if new_valve in current:
                        continue
                    tmp_minutes[i] += tunnel_cost[(candidate, new_valve)]
                    tmp_current = current.copy()
                    tmp_current[i] = new_valve
                    best = max(best, try_valve2(valves, id_to_int, tunnel_cost, tmp_open_valves, tmp_current, tmp_minutes, tmp_score))
                    tmp_minutes[i] -= tunnel_cost[(candidate, new_valve)]

    #global best_score_yet
    #if best > best_score_yet:
    #    print(best)
    #best_score_yet = max(best_score_yet, best)

    #if len(cache) < 100000000:
    cache[key] = best
    return best



def main():

    lines = open_data("16.data")

    id_to_int = dict()
    tunnel_cost = dict()
    valves = dict()
    for i, line in enumerate(lines):
        l = line.split(" ")
        v = l[1]
        flow_rate = ints(line)[0]
        vs = line.split(" to ")[1].replace(",", "").split(" ")[1:]
        valves[v] = Valve(flow_rate, set(vs))
        for v2 in vs:
            tunnel_cost[(v,v2)] = 1
        id_to_int[v] = i

    to_delete = []
    for k,v in valves.items():
        if k != "AA" and v.flow_rate == 0:
            to_delete.append(k)
            for v1 in v.tunnels:
                for v2 in v.tunnels:
                    if v1 != v2:
                        valves[v1].tunnels.remove(k)
                        valves[v1].tunnels.add(v2)
                        valves[v2].tunnels.add(v1)
                        tunnel_cost[(v1,v2)] = tunnel_cost[(v1,k)] + tunnel_cost[(k, v2)]
    for k in to_delete:
        del valves[k]

    print(try_valve2(valves, id_to_int, tunnel_cost, "", ["AA", "AA"], [0, 0], 0))


if __name__ == "__main__":
    main()

# year 2022
# solution for 16.01: 2265
# solution for 16.02: 2811
