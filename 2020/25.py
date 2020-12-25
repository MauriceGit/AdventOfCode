#!/usr/bin/env python3.7

from utility import *


 # https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def main():

    lines = open_data("25.data")

    c_p, d_p = ints(lines)


    # modinv(5764801, 20201227) = 7^n
    print(round(math.log(modinv(5764801,  20201227))/math.log(7)))

    # 5249543 = 7^x % 2020122
    x = 8419519

    print(pow(14082811, x) % 20201227)


if __name__ == "__main__":
    main()

# solution for 25.01: 3217885
# solution for 25.02: :)
