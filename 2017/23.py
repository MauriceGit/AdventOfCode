#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *


def debug_run(regs, lines):
    count_mul = 0
    i = 0
    while True:
        if i >= len(lines) or i < 0:
            return count_mul
        t = lines[i].split(" ")
        op = t[0]
        r1 = t[1] if t[1] in regs else int(t[1])
        r2 = 0 if len(t) <= 2 else regs[t[2]] if t[2] in regs else int(t[2])
        jump = 1

        if op == "set":
            regs[r1] = r2
        elif op == "sub":
            regs[r1] -= r2
        elif op == "mul":
            regs[r1] *= r2
            count_mul += 1
        elif op == "jnz" and regs[r1] != 0 if r1 in regs else r1 != 0:
            jump = r2
        i += jump

    return count_mul


# https://stackoverflow.com/questions/15285534/isprime-function-for-python-language
def is_prime(n):
    """"pre-condition: n is a nonnegative integer
    post-condition: return True if n is prime and False otherwise."""
    if n < 2:
         return False;
    if n % 2 == 0:
         return n == 2  # return False
    k = 3
    while k*k <= n:
         if n % k == 0:
             return False
         k += 2
    return True


def run():
    return sum(not is_prime(x) for x in range(106700, 123700+1, 17))


def main():
    print(debug_run({r:0 for r in "abcdefgh"}, open_data("23.data")))
    print(run())


if __name__ == "__main__":
    main()

# year 2017
# solution for 23.01: 4225
# solution for 23.02: 905
