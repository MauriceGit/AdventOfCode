#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


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
        return _parse_immune_weak(a), _parse_immune_weak(b)
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


def calc_damage(g, attacker):
    if g.team == attacker.team:
        return (0, 0, 0)
    dmg = attacker.count * attacker.damage
    if attacker.damage_type in g.immune:
        dmg = 0
    if attacker.damage_type in g.weak:
        dmg *= 2
    return (dmg, g.count*g.damage, g.initiative)


# returns (key, group)
def find_target(attacker, groups):

    def sort_key(g):
        return calc_damage(g[1], attacker)
    tmp = sorted(groups, key=sort_key, reverse=True)
    dmg = calc_damage(tmp[0][1], attacker)[0]
    if dmg == 0:
        return -1, None
    return tmp[0]


def pp(groups):
    def _pp(k, p):
        print(f"  {k: >2}: {p.count : <4} hp: {p.hit_points: <5} weak: {str(p.weak): <28} immune: {str(p.immune): <33} damage: {p.damage: <4} damage_type: {p.damage_type:<11} initiative: {p.initiative}")
    print("Immunity:")
    for k, p in groups.items():
        if p.team == 0:
            _pp(k, p)
    print("Infection:")
    for k, p in groups.items():
        if p.team == 1:
            _pp(k, p)
    print()

def main():

    immune, infect = open_data_groups("24.data")
    immune, infect = immune[1:], infect[1:]

    groups = dict()
    for i, g in enumerate(immune):
        groups[i] = parse_attributes(g, 0)
    for i, g in enumerate(infect):
        groups[i+len(immune)] = parse_attributes(g, 1)

    # as long as we have two teams!
    while not all(g.team == list(groups.values())[0].team for g in groups.values()):

        indices = list(groups.keys())
        indices.sort(key=lambda i: (groups[i].count*groups[i].damage, groups[i].initiative), reverse=True)

        pp(groups)

        # target selection
        selection = defaultdict(lambda: -1)
        for i in indices:
            key, target = find_target(groups[i], [(k,v) for k,v in groups.items() if k not in selection.values()])
            if target != None:
                selection[i] = (key, calc_damage(target, groups[i])[0])

        # attacking
        indices.sort(key=lambda i: groups[i].initiative, reverse=True)
        for i in indices:
            attacker = groups[i] if i in groups else None
            print(selection[i])
            if attacker != None and selection[i][0] != -1:
                index, dmg = selection[i]
                defender = groups[index]
                #dmg = calc_damage(defender, attacker)[0]
                killed_units = int(dmg // defender.hit_points)

                groups[index].count -= killed_units
                if groups[index].count <= 0:
                    del groups[index]


        #return

    print(groups)
    print(sum(g.count for g in groups.values()))

    # > 742

if __name__ == "__main__":
    main()

# year 2018
# solution for 24.01: ?
# solution for 24.02: ?
