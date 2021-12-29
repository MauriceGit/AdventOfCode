#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *


def interpret(lines, number):

    i = 0
    arr = [0,0,0,0]
    v = {"x":0, "y":1, "z":2, "w":3}

    def n(x):
        if x.isdigit() or x.startswith("-"):
            return int(x)
        return arr[v[x]]

    ops = {
        "add": lambda a,b: a+b,
        "mul": lambda a,b: a*b,
        "div": lambda a,b: a//b,
        "mod": lambda a,b: a%b,
        "eql": lambda a,b: int(a==b)
    }

    for l in lines:
        if l.startswith("inp"):
            op, w = l.split(" ")
            arr[v[w]] = int(number[i])
            i += 1
        else:
            op, a, b = l.split(" ")
            arr[v[a]] = ops[op](n(a), n(b))

    return arr[2]


def pp(lines):

    op_1 = {"add": "+", "mul": "*", "div": "//"}
    op_2 = {"mod": "{} % {}", "eql": "int({} == {})"}

    print("x,y,z,w = 0,0,0,0")
    i = 0
    for l in lines:
        if l.startswith("inp"):
            _, w = l.split(" ")
            print("{} = INPUT_{}".format(w, i))
            i += 1
        else:
            op, a, b = l.split(" ")
            if op in op_1.keys():

                if op == "mul" and b.isdigit() and int(b) == 0:
                    print("{} = 0".format(a))
                else:
                    print("{} {}= {}".format(a, op_1[op], b))
            else:
                print("{} = {}".format(a, op_2[op].format(a, b)))


def test(number):
    x,z,w = 0,0,0
    number = list(number)

    w = int(number[0])
    z = w + 2

    w = int(number[1])
    z *= 26
    z += w + 4

    w = int(number[2])
    z *= 26
    z += w + 8

    w = int(number[3])
    z *= 26
    z += w + 7

    w = int(number[4])
    z *= 26
    z += w + 12

    x = z % 26
    z //= 26
    x += -14
    if x <= 0 or x > 9:
        return None
    number[5] = str(x)

    x = z % 26
    z //= 26
    if x <= 0 or x > 9:
        return None
    number[6] = str(x)

    w = int(number[7])
    z *= 26
    z += w + 14

    x = z % 26
    z //= 26
    x += -10
    if x <= 0 or x > 9:
        return None
    number[8] = str(x)

    w = int(number[9])
    z *= 26
    z += w + 6

    x = z % 26
    z //= 26
    x += -12
    if x <= 0 or x > 9:
        return None
    number[10] = str(x)

    x = z % 26
    z //= 26
    x += -3
    if x <= 0 or x > 9:
        return None
    number[11] = str(x)

    x = z % 26
    z //= 26
    x += -11
    if x <= 0 or x > 9:
        return None
    number[12] = str(x)

    x = z % 26
    z //= 26
    x += -2
    if x <= 0 or x > 9:
        return None
    number[13] = str(x)

    return None if z != 0 else number


# Only takes half a second, don't worry ;)
def try_combination(possible_numbers):

    n = "{}{}{}{}{}__{}_{}____"
    for c0 in possible_numbers:
        for c1 in possible_numbers:
            for c2 in possible_numbers:
                for c3 in possible_numbers:
                    for c4 in possible_numbers:
                        for c5 in possible_numbers:
                            for c6 in possible_numbers:
                                tmp = test(n.format(c0, c1, c2, c3, c4, c5, c6))
                                if tmp is not None:
                                    return "".join(tmp)
    return None


def main():

    # pp() was used to transform the input to python code to make it easier to work with
    # The transformed code was then simplified manually
    # interpret() was used to verify, that my simplifications were valid

    # Then: Half of the input numbers must match x when compared (eql), so that x == 0 afterwards.
    # That is needed, so that z stays as small as possible and doesn't explode!
    # So those numbers can just be assigned x. The actual input does not need to be computed!

    # If at any place, we get comparisons outside our range, the number is invalid and we return early.
    # Otherwise we just try the remaining values from top or bottom depending on part1 or part2.

    # The first result (part 1) was determined completely manually by going through some numbers with
    # the first ones having a higher priority. It took about 10 minutes to get the correct result.
    # Afterwards I automated that process for part 2. It computes both parts in ~1.3s now.

    lines = open_data("24.data")

    print(try_combination("987654321"))
    print(try_combination("123456789"))


if __name__ == "__main__":
    main()

# year 2021
# solution for 24.01: 99429795993929
# solution for 24.02: 18113181571611
