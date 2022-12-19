#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

# bots: (ore_robot, clay_robot, obisidian_robot, geode_robot)
# ores: (ore, clay, obsidian, geode)
cache = dict()
best_result = 0

def run_blueprint(bp, max_needed, ores, bots, minute, max_minutes):
    global best_result

    if minute >= max_minutes:
        return ores[3]

    o = ores[0]<<18|ores[1]<<12|ores[2]<<6|ores[3]
    b = bots[0]<<18|bots[1]<<12|bots[2]<<6|bots[3]
    key = o<<30 | b<<6 | minute
    if key in cache:
        return cache[key]

    n = max_minutes-minute
    upper_range = n*(n+1)//2
    if ores[3]+bots[3]*n+upper_range < best_result:
        cache[key] = ores[3]
        return ores[3]

    best = ores[3]
    # if we can build a geode robot, we only do that!
    if ores[2] >= bp[3][2] and ores[0] >= bp[3][0]:
        best = max(best, run_blueprint(bp, max_needed, add(bots, sub(ores, bp[3])), add(bots, (0,0,0,1)), minute+1, max_minutes))
        cache[key] = best
        return best

    count = 0
    for bi, b in reversed(list(enumerate(bp[:3]))):
        ok = True
        for i, ore in enumerate(b):
            if ores[i] < ore:
                ok = False
                break
        if ok:
            # heuristic: If we have twice of this ore than we would need for anything,
            # we don't want to produce even more! So no more bot for this!
            if ores[bi] >= 1.5*max_needed[bi]:
                continue
            count += 1
            new_bot = tuple([int(i==bi) for i in range(4)])
            best = max(best, run_blueprint(bp, max_needed, add(bots, sub(ores, bp[bi])), add(bots, new_bot), minute+1, max_minutes))

    if count < 3:
        best = max(best, run_blueprint(bp, max_needed, add(bots, ores), bots, minute+1, max_minutes))

    cache[key] = best
    best_result = max(best_result, best)
    return best


def main():

    lines = open_data("19.data")

    blueprints = []
    for l in lines:
        g = l.split("Each")
        tmp2 = ints(g[3])
        tmp3 = ints(g[4])
        blueprints.append(((ints(g[1])[0],0,0,0), ((ints(g[2])[0],0,0,0)), (tmp2[0], tmp2[1], 0,0), (tmp3[0], 0, tmp3[1],0)))

    global best_result
    quality = 0
    for i,bp in enumerate(blueprints):
        cache.clear()
        best_result = 0
        max_needed = [max(bp, key=lambda x: x[i])[i] for i in range(4)]
        r = run_blueprint(bp, max_needed, [0,0,0,0], [1,0,0,0], 0, 24)
        #print(f"Blueprint {i+1} can create {r} geodes")
        quality += (i+1)*r
    print(quality)

    part2 = 1
    for i,bp in enumerate(blueprints[:3]):
        cache.clear()
        best_result = 0
        max_needed = [max(bp, key=lambda x: x[i])[i] for i in range(4)]
        r = run_blueprint(bp, max_needed, [0,0,0,0], [1,0,0,0], 0, 32)
        part2 *= r
    print(part2)


if __name__ == "__main__":
    main()

# year 2022
# solution for 19.01: 1306
# solution for 19.02: 37604
