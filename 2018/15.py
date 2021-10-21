#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *
import copy


# bfs with one specific target position!
def bfs_target(field, units, start_pos, target_pos):
    reading_order = [(0,-1), (-1,0), (1,0), (0,1)]
    backtrack = {start_pos: -1}
    visited = set([u[0] for u in units])
    candidates = [start_pos]

    while len(candidates) > 0:
        c = candidates.pop(0)
        if c == target_pos:
            break

        for r in reading_order:
            new_pos = add(c,r)
            if new_pos in visited or new_pos not in field:
                continue

            candidates.append(new_pos)
            backtrack[new_pos] = c
            visited.add(new_pos)

    if target_pos not in backtrack:
        return (None, 100000)

    path = []
    p = target_pos
    while backtrack[p] != -1:
        path.append(p)
        p = backtrack[p]

    return (path[-1], len(path)+1) if len(path) > 0 else (None, 100000)


def bfs(field, units, current_pos, team):

    reading_order = [(0,-1), (-1,0), (1,0), (0,1)]
    enemies = [u[0] for u in units if u[2] != team]
    enemies.sort(key=lambda x: (x[1], x[0]))
    used_positions = {u[0] for u in units}

    best_step = None
    min_distance = 100000

    for e in enemies:
        for r in reading_order:
            p = add(e, r)
            if p in field and p not in used_positions:
                step, dist = bfs_target(field, units, current_pos, p)
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


def run(lines):
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


def main():

    groups = open_data_groups("15.data")

    for g in groups:
        run(g)
        print()


if __name__ == "__main__":
    main()

# year 2018
# solution for 15.01: 257954
# solution for 15.02: 51041
