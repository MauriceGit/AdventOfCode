#!/usr/bin/env python3.7

from utility import *

def check(r, t, i):
    return r[0][0] <= t[i] <= r[0][1] or r[1][0] <= t[i] <= r[1][1]

def invalid_passes(rules, ticket):

    res = 0
    for i in range(len(ticket)):
        if all([not check(r, ticket, i) for r in rules.values()]):
            res += ticket[i]

    return res


def try_index(rules, index, tickets):

    keys = set()
    for k in rules:
        if all([check(rules[k], t, index) for t in tickets]):
            keys.add(k)

    return keys

def main():

    lines = open_data_groups("16.data")

    rules = dict()
    for l in lines[0]:
        r = re.match(r"([a-z ]+): (\d+)-(\d+) or (\d+)-(\d+)", l)
        rules[r.group(1)] = [(int(r.group(2)),int(r.group(3))), (int(r.group(4)),int(r.group(5)))]


    good_tickets = []
    invalid_count = 0
    for l in lines[2][1:]:
        invalid = invalid_passes(rules, ints(l))
        invalid_count += invalid
        if invalid == 0:
            good_tickets.append(ints(l))

    # Puzzle 1
    print(invalid_count)

    valid_keys = [try_index(rules, i, good_tickets) for i in range(len(good_tickets[0]))]

    key_index = [""] * len(valid_keys)
    while True:
        change = False
        for i, k in enumerate(valid_keys):
            if len(k) == 1:

                # remove the found key from all other sets
                for j in range(len(valid_keys)):
                    valid_keys[j] = valid_keys[j]-k
                # save it in result list
                key_index[i] = list(k)[0]
                change = True
                break
        if not change:
            break


    my_passport = ints(lines[1][1])
    result = 1
    for i, k in enumerate(key_index):
        if k.startswith("departure"):
            result *= my_passport[i]

    # Puzzle 2
    print(result)



if __name__ == "__main__":
    main()

# solution for 16.01: 24110
# solution for 16.02: 6766503490793
