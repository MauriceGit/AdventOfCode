#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def main():

    lines = open_data("07.data")

    d = defaultdict(set)
    ids = set()
    for l in lines:
        s = l.split(" ")
        d[s[7]].add(s[1])
        ids.add(s[1])

    orig_d = d.copy()

    next_ids = sorted(ids - set(d.keys()))
    done_ids = set()

    steps = ""
    while len(next_ids) > 0:
        e = next_ids.pop(0)
        steps += e
        done_ids.add(e)

        d = {k:v-{e} for k,v in d.items()}

        next_ids = sorted((set(next_ids) | {k for k in d.keys() if d[k] == set()}) - done_ids)

    print(steps)

    d = orig_d

    tmp = [(i, ord(i)-4) for i in ids - set(d.keys())]
    next_ids = sorted(tmp, key=lambda x: [x[1], x[0]])
    done_ids = set()

    steps = ""
    time = 0
    while len(next_ids) > 0:

        # decrease the first 5 tasks by 1 second
        for i, t in enumerate(next_ids[:5]):
            next_ids[i] = (next_ids[i][0], next_ids[i][1]-1)

        removed = set()
        for i, t in enumerate(reversed(next_ids)):
            if t[1] <= 0:
                done_ids.add(t[0])
                steps += t[0]
                removed.add(t[0])

        d = {k:v-removed for k,v in d.items()}

        # remove finished tasks
        for i, t in enumerate(reversed(next_ids)):
            if t[1] <= 0 or t[0] in done_ids:
                del next_ids[next_ids.index(t)]

        # add new tasks
        for k in d.keys():
            if d[k] == set():
                found = [1 for n in next_ids if n[0] == k]
                if not found:
                    next_ids.append((k, ord(k)-4))

        for n in next_ids.copy():
            if n[0] in done_ids:
                del next_ids[next_ids.index(n)]

        next_ids = sorted(set(next_ids)-done_ids, key=lambda x: [x[1], x[0]])
        time += 1

    print(time)


if __name__ == "__main__":
    main()

# year 2018
# solution for 07.01: BGKDMJCNEQRSTUZWHYLPAFIVXO
# solution for 07.02: 941
