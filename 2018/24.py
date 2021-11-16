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
    return teams[0] == 0 or teams[1] == 0



def main():

    immune, infect = open_data_groups("24.data")
    immune, infect = immune[1:], infect[1:]

    groups = dict()
    for i, g in enumerate(immune):
        groups[i] = parse_attributes(g, 0)
    for i, g in enumerate(infect):
        groups[i+len(immune)] = parse_attributes(g, 1)

    # as long as we have two teams!
    while not someone_won(groups):

        indices = list(groups.keys())
        indices.sort(key=lambda i: (groups[i].count*groups[i].damage, groups[i].initiative), reverse=True)

        pp(groups)

        #for k, g in groups.items():
        #    for k2, g2 in groups.items():
        #        if g.team != g2.team:
        #            dmg = calc_damage(g2, g)[0]
        #            print(f"{'Infection' if g.team else 'Immune System'} group {k} would deal defending group {k2} {dmg} damage")
        #print()

        # target selection
        selection = defaultdict(lambda: -1)
        for i in indices:
            if groups[i].count > 0:
                key, target = find_target(groups[i], [(k,v) for k,v in groups.items() if k not in selection.values()])
                if target != None and key != -1:
                    selection[i] = key

        # attacking
        indices.sort(key=lambda i: groups[i].initiative, reverse=True)
        for i in indices:
            #if groups[i].count > 0:
                attacker = groups[i] if i in groups else None
                if attacker != None and i in selection and selection[i] != -1:
                    index = selection[i]
                    defender = groups[index]
                    dmg = calc_damage(defender, attacker)[0]
                    killed_units = int(dmg // defender.hit_points)
                    #killed_units = dmg
                    if killed_units > defender.count:
                        killed_units = defender.count

                    #print(f"{'Infection' if attacker.team else 'Immune System'} group {i} attacks group {index}, killing {killed_units} units - {dmg}")

                    groups[index].count -= killed_units
                    if groups[index].count <= 0:
                        groups[index].count = 0
                        del groups[index]


        #print("\n=================================================\n")


    pp(groups)
    print(sum(g.count for g in groups.values()))

    # > 742

if __name__ == "__main__":
    main()

# year 2018
# solution for 24.01: ?
# solution for 24.02: ?
