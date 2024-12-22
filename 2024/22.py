#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def next_secret_number(secret):
    secret = (secret ^ (secret << 6)) % 16777216
    secret = (secret ^ (secret >> 5)) % 16777216
    secret = (secret ^ (secret << 11)) % 16777216
    return secret

def all_prices(secret):
    prices = [secret%10]
    for i in range(2000):
        secret = next_secret_number(secret)
        prices.append(secret%10)
    return prices

def diff_to_dict(prices):
    diffs = dict()
    dl = []
    for i in range(1, len(prices)):
        dl.append(prices[i]-prices[i-1])
        if i >= 4:
            diff = f"{dl[-4]},{dl[-3]},{dl[-2]},{dl[-1]}"
            # Only account for the first occurence!
            if diff not in diffs:
                diffs[diff] = prices[i]
    return diffs

def find_best_diff(all_diffs):
    # lets assemble a set of ALL unique diffs to iterate over!
    diffs = set()
    for d in all_diffs:
        diffs |= set(d.keys())

    best_sum = 0
    for d in diffs:
        best_sum = max(sum(diff[d] for diff in all_diffs if d in diff), best_sum)
    return best_sum

def main():

    lines = lmap(int, open_data("22.data"))

    s = 0
    for secret in lines:
        for i in range(2000):
            secret = next_secret_number(secret)
        s += secret
    print(s)

    all_diffs = lmap(lambda x: diff_to_dict(all_prices(x)), lines)
    print(find_best_diff(all_diffs))


if __name__ == "__main__":
    main()

# year 2024
# solution for 22.01: 13764677935
# solution for 22.02: 1619
