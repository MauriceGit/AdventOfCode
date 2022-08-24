#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


Particle = recordtype("Particle", "p v a move_away")

def same_dir(a, v):
    return a[0]*v[0] >= 0 and a[1]*v[1] >= 0 and a[2]*v[2] >= 0


def main():
    lines = lmap(ints, open_data("20.data"))

    particles = [Particle(tuple(l[:3]), tuple(l[3:6]), tuple(l[6:9]), False) for l in lines]

    # The winner is the one with the smallest acceleration. If equal, the smallest velocity.
    # it is the one that will move slowest and so stay closer to zero!
    print(min(list(enumerate(particles)), key=lambda x: (sum(map(abs, x[1].a)), sum(map(abs, x[1].v))))[0])

    while True:
        positions = defaultdict(set)
        all_move_away = True
        for i,p in enumerate(particles):
            tmp_p = p.p
            particles[i].v = add(p.v, p.a)
            particles[i].p = add(p.p, p.v)

            positions[p.p].add(i)

            d1 = manhatten_length(p.p)
            d2 = manhatten_length(tmp_p)

            particles[i].move_away = d1 > d2 and same_dir(p.a, p.v)
            all_move_away = all_move_away and p.move_away

        collisions = set().union(*list(filter(lambda x: len(x) > 1, positions.values())))
        for i in sorted(list(collisions), reverse=True):
            particles.pop(i)

        if all_move_away:
            break

    print(len(particles))


if __name__ == "__main__":
    main()

# year 2017
# solution for 20.01: 344
# solution for 20.02: 404
