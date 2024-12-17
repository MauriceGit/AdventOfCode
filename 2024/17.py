#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

def combo(regs, operand):
    if operand <= 3:
        return operand
    return regs[operand-4]

def run(regs, prog):
    instr = 0
    out = []
    while instr < len(prog):

        op = prog[instr]
        operand = prog[instr+1]
        incr = 2

        match op:
            case 0:  # adv
                regs[0] = regs[0] // 2**combo(regs, operand)
            case 1:  # bxl
                regs[1] = regs[1] ^ operand
            case 2:  # bst
                regs[1] = combo(regs, operand) % 8
            case 3:  # jnz
                if regs[0] != 0:
                    instr = operand
                    incr = 0
            case 4:  # bxc
                regs[1] = regs[1] ^ regs[2]
            case 5:  # out
                out.append(combo(regs, operand)%8)
            case 6:  # bdv
                regs[1] = regs[0] // 2**combo(regs, operand)
            case 7:  # cdv
                regs[2] = regs[0] // 2**combo(regs, operand)
        instr += incr

    return ",".join(map(str, out))


def run2(a):
    l = []
    while a > 0:
        # last 3 bits with the first bit flipped
        left = (a%8) ^ 4
        # power is <= 7. Denominator is <= 128
        # removes <= 7 bits from the end! (right shift!)
        right = a // 2**((a%8)^1)
        # only the last 3 bits matter at all!
        v = (left ^ right) % 8
        l.append(v)
        # right shift 3 bits! --> Figure out the number in 3-bit increments!
        a //= 8
    return l


def try_combinations(number, expected):

    if len(expected) == 0:
        return int(number, 2)

    for i in range(8):
        tmp = number + bin(i)[2:].zfill(3)
        if run2(int(tmp, 2))[0] == expected[-1]:
            if (res := try_combinations(tmp, expected[:-1])) is not None:
                return res

    return None


def main():

    regs, prog = open_data_groups("17.data")
    regs = lmap(lambda x: x[0], map(ints, regs))
    prog = ints(prog[0])

    print(",".join(map(str, run2(regs[0]))))
    print(try_combinations("100", prog[:-1]))


if __name__ == "__main__":
    main()

# year 2024
# solution for 17.01: 5,0,3,5,7,6,1,5,4
# solution for 17.02: 164516454365621
