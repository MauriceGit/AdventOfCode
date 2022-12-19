#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

# bots: (ore_robot, clay_robot, obisidian_robot, geode_robot)
# ores: (ore, clay, obsidian, geode)
best_result = 0
cache = dict()
def run_blueprint(bp, ores, bots, minute):

    if minute >= 24:
        return ores[3]

    o = ores[0]<<18|ores[1]<<12|ores[2]<<6|ores[3]
    b = bots[0]<<18|bots[1]<<12|bots[2]<<6|bots[3]
    key = o<<30 | b<<6 | minute
    #key = ores[3]<<30 | b<<6 | minute
    #key = (tuple(ores), tuple(bots), minute)
    if key in cache:
        return cache[key]

    #print(ores, bots, minute)

    #possible_new_bots = []
    #for bi, b in enumerate(bp):
    #    ok = True
    #    for i, ore in enumerate(b):
    #        if ores[i] < ore:
    #            ok = False
    #            break
    #    if ok:
    #        # (bp_index, (0,1,0,0)) for clay robot
    #        t = (bi, tuple([1 if i==bi else 0 for i in range(4)]))
    #        possible_new_bots.append(t)
    #
    ## one ore for each bot we have for each ore.
    #ores = add(ores, bots)
    new_ores = bots
    #
    #if len(possible_new_bots) < 4:
    #    best = run_blueprint(bp, ores, bots, minute+1)
    #else:
    #    best = ores[3]
    #
    #for bi, b in reversed(possible_new_bots):
    #    #print(f"{ores} - {bp[bi]} | {bots} + {b}")
    #    best = max(best, run_blueprint(bp, sub(ores, bp[bi]), add(bots, b), minute+1))

    best = ores[3]
    tried_something = False
    # if we can build a geode robot, we only do that!
    if ores[2] >= bp[3][2] and ores[0] >= bp[3][0]:
        best = max(best, run_blueprint(bp, add(new_ores, sub(ores, bp[3])), add(bots, (0,0,0,1)), minute+1))
        tried_something = True
    elif(ores[1] >= bp[2][1] and ores[0] >= bp[2][0]):
        best = max(best, run_blueprint(bp, add(new_ores, sub(ores, bp[2])), add(bots, (0,0,1,0)), minute+1))
        tried_something = True
    else:
        for bi, b in enumerate(bp[:2]):
            ok = True
            for i, ore in enumerate(b):
                if ores[i] < ore:
                    ok = False
                    break
            if ok:
                new_bot = tuple([int(i==bi) for i in range(4)])
                best = max(best, run_blueprint(bp, add(new_ores, sub(ores, bp[bi])), add(bots, new_bot), minute+1))
                tried_something = True

        best = max(best, run_blueprint(bp, add(new_ores, ores), bots, minute+1))




    cache[key] = best
    global best_result
    if best > best_result:
        best_result = best
        print(best_result)

    return best



def main():

    lines = open_data("19.data")

    blueprints = []
    for l in lines:
        g = l.split("Each")
        tmp2 = ints(g[3])
        tmp3 = ints(g[4])
        blueprints.append(((ints(g[1])[0],0,0,0), ((ints(g[2])[0],0,0,0)), (tmp2[0], tmp2[1], 0,0), (tmp3[0], 0, tmp3[1],0)))




    quality = 0
    for i,bp in enumerate(blueprints):
        r = run_blueprint(bp, [0,0,0,0], [1,0,0,0], 0)
        print(f"Blueprint {i+1} can create {r} geodes")
        quality += (i+1)*r
        cache.clear()
        global best_result
        best_result = 0
    print(f"Overall quality: {quality}")


if __name__ == "__main__":
    main()

# year 2022
# solution for 19.01: ?
# solution for 19.02: ?
