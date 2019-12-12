import re
from itertools import combinations, permutations
from collections import namedtuple

def add(a,b):
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

if __name__ == "__main__":

    with open("12.data", "r") as f:

        Planet = namedtuple("Planet", "p v")
        planets = []

        for p in f.read().splitlines():
            # regex on what to replace
            rx = re.compile("([<>=, ])")
            # replace all of it with "" and split coordinates. First one is empty because of leading x
            planets.append(Planet(tuple(map(int, re.split("x|y|z", rx.sub("", p))[1:])), (0,0,0)))

        print(planets)
        #print(list(combinations(range(len(planets)), 2)))
        #print(list(permutations(range(len(planets)), 2)))
