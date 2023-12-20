#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def run(conjunctions, flipflops, broadcaster):
    queue = SimpleQueue()
    # (from, to, pulse)
    queue.put(("", "broadcaster", False))
    pulse_count = [0,0]

    while not queue.empty():
        source, dest, signal = queue.get()
        pulse_count[signal] += 1

        if dest == "broadcaster":
            for to in broadcaster:
                queue.put(("broadcaster", to, signal))
        else:
            if dest in flipflops and signal == False:
                flipflops[dest] = (not flipflops[dest][0], flipflops[dest][1])
                for to in flipflops[dest][1]:
                    queue.put((dest, to, flipflops[dest][0]))
            if dest in conjunctions:
                conjunctions[dest][0][source] = signal
                value = all(conjunctions[dest][0].values())
                for to in conjunctions[dest][1]:
                    queue.put((dest, to, not value))

    return tuple(pulse_count)


def find_loop(conjunctions, flipflops, broadcaster, k0, k1, part1=False):

    old_value = False
    old_i = 0
    loop = []
    pulse_count = (0,0)
    for i in itertools.count():
        low, high = run(conjunctions, flipflops, broadcaster)
        pulse_count = add(pulse_count, (low, high))
        if part1 and i == 1000-1:
            return pulse_count[0]*pulse_count[1]
        # Just look at state-changes!
        if not part1 and conjunctions[k0][0][k1] != old_value:
            # the first iteration is just off. So we ignore that!
            if old_i != 0:
                loop.append(abs(i-old_i))

            if len(set(loop)) >= 2 and len(loop)%2 == 0:
                if loop[:len(loop)//2] == loop[len(loop)//2:]:
                    return sum(loop[:len(loop)//2])
            old_i = i
            old_value = conjunctions[k0][0][k1]
    return 1


def main():

    lines = open_data("20.data")

    conjunctions = dict()
    flipflops = dict()
    broadcaster = []

    # reverse mapping for key retrieval and conjunctions
    to_from = defaultdict(list)

    for line in lines:
        fr, to = line.split(" -> ")
        fr = fr if fr == "broadcaster" else fr[1:]
        to = to.split(", ")

        for t in to:
            to_from[t].append(fr)

        if fr == "broadcaster":
            broadcaster = to
        else:
            if line[0] == "%":
                flipflops[fr] = (False, to)
            else:
                conjunctions[fr] = (None, to)

    for k,(_, to) in conjunctions.items():
        tmp = dict(zip(to_from[k], [False]*len(to_from[k])))
        conjunctions[k] = (tmp, to)

    # The loop is identical for all 'bit'-states leading to k (2 states before rx).
    # So we are good with calculating just one single loop for each of the four states leading to rx.
    loops = [(k, to_from[k][0]) for k in [to_from[s][0] for s in to_from[to_from["rx"][0]]]]

    print(find_loop(deepcopy(conjunctions), flipflops, broadcaster, None, None, part1=True))
    res = {find_loop(deepcopy(conjunctions), flipflops, broadcaster, l[0], l[1]) for l in loops}
    print(lcm(*res))


if __name__ == "__main__":
    main()

# year 2023
# solution for 20.01: 812721756
# solution for 20.02: 233338595643977
