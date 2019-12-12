import re
from itertools import combinations, permutations
from recordtype import recordtype
import time
import copy
from fractions import gcd
from collections import defaultdict

def add(a,b):
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def mul(a,f):
    return (a[0]*f, a[1]*f, a[2]*f)

# compare like in C. -1, 0, 1
def cmp(x1, x2):
    return 0 if x1 == x2 else 1 if x2-x1 > 0 else -1

def gravity(p1, p2):
    return (cmp(p1[0],p2[0]), cmp(p1[1],p2[1]), cmp(p1[2],p2[2]))

def energy(t):
    return abs(t[0])+abs(t[1])+abs(t[2])

def tot_energy(p):
    # potential * kinetic
    return energy(p.p) * energy(p.v)

def to_hashable(p):
    return (p.p, p.v)


# Checks how many times l is a subset of l2
def subset_cnt(l, l2):
    return len(list(filter(lambda x: x != -1, [i if l[i:i+len(l2)] == l2 else -1 for i in range(len(l)-len(l2))])))

def update_planets(planets):
    # Update velocity
    for p in planets:
        for p2 in planets:
            p.v = add(p.v, gravity(p.p, p2.p))

    # change position
    for p in planets:
        p.p = add(p.p, p.v)

def lcm(a,b):
    return (a*b)//gcd(a,b)

if __name__ == "__main__":

    with open("12.data", "r") as f:

        Planet = recordtype("Planet", "p v")
        planets = []

        for p in f.read().splitlines():
            # regex on what to replace
            rx = re.compile("([<>=, ])")
            # replace all of it with "" and split coordinates. First one is empty because of leading x
            planets.append(Planet(tuple(map(int, re.split("x|y|z", rx.sub("", p))[1:])), (0,0,0)))


        # let's just assume, that a cycle is a minimum of 50 individual calculated steps...
        n = 50

        first_n_hash = dict()
        last_n_coordinate_values = defaultdict(list)
        cycle_times_per_coordinate = dict()


        i = 0
        while(True):

            if i == n:
                first_n_hash["x"] = hash(tuple(last_n_coordinate_values["x"]))
                first_n_hash["y"] = hash(tuple(last_n_coordinate_values["y"]))
                first_n_hash["z"] = hash(tuple(last_n_coordinate_values["z"]))

            if i > n:
                if hash(tuple(last_n_coordinate_values["x"])) == first_n_hash["x"]:
                    cycle_times_per_coordinate["x"] = i-n
                if hash(tuple(last_n_coordinate_values["y"])) == first_n_hash["y"]:
                    cycle_times_per_coordinate["y"] = i-n
                if hash(tuple(last_n_coordinate_values["z"])) == first_n_hash["z"]:
                    cycle_times_per_coordinate["z"] = i-n

            if i >= n:
                last_n_coordinate_values["x"].pop(0)
                last_n_coordinate_values["y"].pop(0)
                last_n_coordinate_values["z"].pop(0)

            last_n_coordinate_values["x"].append(planets[0].p[0])
            last_n_coordinate_values["y"].append(planets[0].p[1])
            last_n_coordinate_values["z"].append(planets[0].p[2])

            # we found all cycle times.
            if len(cycle_times_per_coordinate) == 3:
                break

            if i == 1000:
                # solution to puzzle 1:
                print(sum(map(tot_energy, planets)))

            update_planets(planets)

            i += 1

        # Solution to puzzle 2:
        x = cycle_times_per_coordinate["x"]
        y = cycle_times_per_coordinate["y"]
        z = cycle_times_per_coordinate["z"]
        # least common multiple for all three coordinates!
        print(lcm(lcm(x,y), lcm(x,z)))
