import re
from recordtype import recordtype
from fractions import gcd
from collections import defaultdict

def add(a,b):
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

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
        # This is a really hacky solution with an explicit n!
        n = 50

        first_n_hash = dict()
        last_n_coordinate_values = defaultdict(list)
        cycle_times_per_coordinate = dict()

        i = 0
        while(len(cycle_times_per_coordinate) < 3):

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

            if i == 1000:
                # solution to puzzle 1:
                print(sum(map(tot_energy, planets)))

            update_planets(planets)

            i += 1

        # Solution to puzzle 2:
        # yes, we ignore the velocity cycles at the moment. But it seems, they
        # match the lcm we calculate right now. So no point in checking.
        x = cycle_times_per_coordinate["x"]
        y = cycle_times_per_coordinate["y"]
        z = cycle_times_per_coordinate["z"]
        # least common multiple for all three coordinates!
        print(lcm(lcm(x,y), lcm(x,z)))

# solution for 12.01: 6735
# solution for 12.02: 326489627728984
