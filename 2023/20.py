#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *
from queue import SimpleQueue

def run(conjunctions, flipflops, broadcaster):

    queue = SimpleQueue()

    # (from, to, pulse)
    queue.put(("", "broadcaster", False))

    pulse_count = [0,0]
    rx_low = False

    while not queue.empty():

        source, dest, signal = queue.get()
        pulse_count[signal] += 1
        if dest == "rx" and not signal:
            rx_low = True
            return (0,0), True

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


    return pulse_count, rx_low





def main():

    lines = open_data("20.data")

    conjunctions = dict()
    flipflops = dict()
    broadcaster = []


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


    pulse_count = (0,0)
    for i in itertools.count():
        (low, high), rx_low = run(conjunctions, flipflops, broadcaster)
        pulse_count = add(pulse_count, (low, high))
        if rx_low:
            print(i+1)
            break
        if i == 1000-1:
            print(pulse_count[0]*pulse_count[1])

        if i > 100000:
            #print(flipflops)
            #print(conjunctions)

            for c in conjunctions:
                print(f"{c} -> {conjunctions[c][1]}: ", end="")
                for k,v in conjunctions[c][0].items():
                    print(f"({k}:{'■' if v else 'ʘ'}) ", end="")
                print()
            print()
            print()

        #print(f"\r{i}", end="")




if __name__ == "__main__":
    main()

# year 2023
# solution for 20.01: 812721756
# solution for 20.02: ?
