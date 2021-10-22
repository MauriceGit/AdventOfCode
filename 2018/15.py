#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *
import copy


# bfs with one specific target position!
def bfs_targets(field, units, start_pos, targets):
    reading_order = [(0,-1), (-1,0), (1,0), (0,1)]
    backtrack = {start_pos: -1}
    visited = set([u[0] for u in units])
    candidates = [start_pos]

    while len(candidates) > 0:
        c = candidates.pop(0)
        if c in targets:
            del targets[targets.index(c)]
            if len(targets) == 0:
                break

        for r in reading_order:
            new_pos = add(c,r)
            if new_pos in visited or new_pos not in field:
                continue

            candidates.append(new_pos)
            backtrack[new_pos] = c
            visited.add(new_pos)

    return backtrack


def get_first_step(backtrack, start, target):

    if target not in backtrack:
        return None, 100000

    count = 0
    step = None
    while backtrack[target] != -1:
        step = target
        count += 1
        target = backtrack[target]

    return step, count


def bfs(field, units, current_pos, team):

    reading_order = [(0,-1), (-1,0), (1,0), (0,1)]
    enemies = [u[0] for u in units if u[2] != team]
    enemies.sort(key=lambda x: (x[1], x[0]))
    used_positions = {u[0] for u in units}

    best_step = None
    min_distance = 100000

    targets = [add(e,r) for e in enemies for r in reading_order]
    targets = [e for e in targets if e in field and e not in used_positions]

    # we bundle the bfs and let it run for all targets. That way we already
    # cache the results for all targets with one run instead of n times restarting
    # the bfs again from the start.
    backtrack = bfs_targets(field, units, current_pos, targets.copy())

    for t in targets:
        step, dist = get_first_step(backtrack, current_pos, t)
        if dist < min_distance:
            best_step = step
            min_distance = dist

    return best_step


def get_inrange_target(p, units, team):

    close_enemies = [u for u in units if u[2] != team and length(sub(u[0], p)) == 1]
    close_enemies.sort(key=lambda x: (x[1], x[0][1], x[0][0]))

    if len(close_enemies) == 0:
        return -1

    return units.index(close_enemies[0])


def run_round(field, units, attack_power):

    i = 0
    while i < len(units):
        if all(x[2] == units[0][2] for x in units):
            return False

        target_index = get_inrange_target(units[i][0], units, units[i][2])
        if target_index == -1:
            next_step = bfs(field, units, units[i][0], units[i][2])
            if next_step != None:
                units[i][0] = next_step

            target_index = get_inrange_target(units[i][0], units, units[i][2])
        if target_index != -1:
            units[target_index][1] -= attack_power[units[i][2]]
            if units[target_index][1] <= 0:
                del units[target_index]
                if target_index < i:
                    continue
        i += 1

    return True


def run_fight(units, field, attack_power):
    rounds = 0
    while True:
        units.sort(key=lambda x: (x[0][1], x[0][0]))
        if not run_round(field, units, attack_power):
            break
        rounds += 1

    return rounds * sum(x[1] for x in units)


def main():

    lines = open_data("15.data")
    units = []
    field = dict()

    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if c != "#":
                field[(x,y)] = 1
                if c in "GE":
                    units.append([(x,y), 200, c == "E"])

    print(run_fight(copy.deepcopy(units), field, {True: 3, False: 3}))

    power = 4
    while True:
        cpy = copy.deepcopy(units)
        res = run_fight(cpy, field, {True: power, False: 3})
        if len([x for x in cpy if x[2]]) == len([x for x in units if x[2]]):
            print(res)
            break
        power += 1


if __name__ == "__main__":
    main()

# year 2018
# solution for 15.01: 257954
# solution for 15.02: 51041
