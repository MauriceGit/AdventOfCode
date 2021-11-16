#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *
from copy import deepcopy

Group = recordtype("Group", "team count hit_points immune weak damage damage_type initiative")


def _parse_immune_weak(s):
    s = s.replace("immune to ", "").replace("weak to ", "")
    return s.split(", ")


def parse_immune_weak(s):
    if "(" not in s:
        return [], []
    s = s.split("(")[1].split(")")[0]
    if ";" in s:
        a, b = s.split("; ")
        immune = _parse_immune_weak(a) if "immune" in a else _parse_immune_weak(b)
        weak = _parse_immune_weak(a) if "weak" in a else _parse_immune_weak(b)
        return immune, weak
    if "immune" in s:
        return _parse_immune_weak(s), []
    if "weak" in s:
        return [], _parse_immune_weak(s)
    return [], []


def parse_attributes(s, team):
    count, hit_points, damage, initiative = ints(s)
    damage_type = s.split(" damage")[0].split(" ")[-1]
    immune, weak = parse_immune_weak(s)
    return Group(team, count, hit_points, immune, weak, damage, damage_type, initiative)


def calc_damage(defender, attacker):
    if defender.team == attacker.team:
        return (0, 0, 0)
    dmg = attacker.count * attacker.damage
    if attacker.damage_type in defender.immune:
        dmg = 0
    if attacker.damage_type in defender.weak:
        dmg *= 2
    return (dmg, defender.count*defender.damage, defender.initiative)


def find_target(attacker, groups):
    if len(groups) == 0:
        return -1
    def sort_key(g):
        return calc_damage(g[1], attacker)
    tmp = sorted(groups, key=sort_key, reverse=True)
    if calc_damage(tmp[0][1], attacker)[0] == 0:
        return -1
    return tmp[0][0]


def pp(groups):
    def _pp(k, p):
        print(f"  {k: >2}: {p.count : <4} hp: {p.hit_points: <5} weak: {str(p.weak): <28} immune: {str(p.immune): <33} damage: {p.damage: <4} damage_type: {p.damage_type:<11} initiative: {p.initiative}")
    print("Immune System:")
    for k, p in groups.items():
        if p.team == 0:
            _pp(k, p)
    print("Infection:")
    for k, p in groups.items():
        if p.team == 1:
            _pp(k, p)
    print()


def someone_won(groups):
    teams = [0,0]
    for k, g in groups.items():
        teams[g.team] += g.count
    return not all(teams)


def fight(groups, immune_booster):
    for i, g in groups.items():
        groups[i].damage += immune_booster if g.team == 0 else 0

    # as long as we have two teams!
    while not someone_won(groups):

        indices = list(groups.keys())
        indices.sort(key=lambda i: (groups[i].count*groups[i].damage, groups[i].initiative), reverse=True)

        # target selection
        selection = defaultdict(lambda: -1)
        for i in indices:
            if groups[i].count > 0:
                possible_enemies = [(k,v) for k,v in groups.items() if k not in selection.values() and v.count > 0 and v.team != groups[i].team]
                key = find_target(groups[i], possible_enemies)
                if key != -1:
                    selection[i] = key

        # attacking
        indices.sort(key=lambda i: groups[i].initiative, reverse=True)
        for i in indices:
            if groups[i].count > 0:
                if selection[i] != -1:
                    attacker = groups[i]
                    index = selection[i]
                    defender = groups[index]
                    dmg = calc_damage(defender, attacker)[0]
                    killed_units = int(dmg // defender.hit_points)
                    groups[index].count -= min(defender.count, killed_units)

    # pp(groups)
    return sum(g.count for g in groups.values())


def main():

    immune, infect = open_data_groups("24.data")
    immune, infect = immune[1:], infect[1:]

    groups = dict()
    for i, g in enumerate(immune):
        groups[i] = parse_attributes(g, 0)
    for i, g in enumerate(infect):
        groups[i+len(immune)] = parse_attributes(g, 1)

    print(fight(deepcopy(groups), 0))
    # Carefully hand-selected value :)
    print(fight(deepcopy(groups), 39))


if __name__ == "__main__":
    main()

# year 2018
# solution for 24.01: 10723
# solution for 24.02: 5120
