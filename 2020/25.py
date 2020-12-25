#!/usr/bin/env python3.7

from utility import *

def main():

    lines = open_data("25.data")

    c_p, d_p = ints(lines)

    # d_p = 7^x % 20201227
    #
    # Calc solution via wolfram-alpha:
    # https://www.wolframalpha.com/input/?i=5249543+%3D+%28%287%5Ex%29+mod+20201227%29
    x = 8419519

    print(pow(c_p, x, 20201227))


if __name__ == "__main__":
    main()

# solution for 25.01: 3217885
# solution for 25.02: :)
