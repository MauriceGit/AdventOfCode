#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *

class VM:

    registers = []
    # instruction pointer
    ip = 0
    ip_index = 0
    commands = []
    command_dict = {"addr": 0, "addi": 1, "mulr": 2, "muli": 3, "banr": 4, "bani": 5, "borr": 6, "bori": 7, "setr": 8, "seti": 9, "gtir": 10, "gtri": 11, "gtrr": 12, "eqir": 13, "eqri": 14, "eqrr": 15}
    rev_commands = {v:k for k,v in command_dict.items()}
    ops = [
        lambda r,a,b: r[a] + r[b],      # addr
        lambda r,a,b: r[a] + b,         # addi
        lambda r,a,b: r[a] * r[b],      # mulr
        lambda r,a,b: r[a] * b,         # muli
        lambda r,a,b: r[a] & r[b],      # banr
        lambda r,a,b: r[a] & b,         # bani
        lambda r,a,b: r[a] | r[b],      # borr
        lambda r,a,b: r[a] | b,         # bori
        lambda r,a,b: r[a],             # setr
        lambda r,a,b: a,                # seti
        lambda r,a,b: int(a > r[b]),    # gtir
        lambda r,a,b: int(r[a] > b),    # gtri
        lambda r,a,b: int(r[a] > r[b]), # gtrr
        lambda r,a,b: int(a == r[b]),   # eqir
        lambda r,a,b: int(r[a] == b),   # eqri
        lambda r,a,b: int(r[a] == r[b]),# eqrr
    ]

    def __init__(self, ip_index, registers, commands):
        self.registers = registers[:]
        self.commands = [(self.command_dict[c[0]], *c[1:]) for c in commands]
        self.ip_index = ip_index


    def _pp(self):
        print("[", end="")
        for r in self.registers:
            print(str(r).ljust(10), end="")
        print("]")


    def _apply_opcode(self, opcode, a, b, c):

        self.registers[self.ip_index] = self.ip
        check_index = 0
        cpy = self.registers[check_index]

        self.registers[c] = self.ops[opcode](self.registers, a, b)

        # Uncomment to see the output that made it easy to see the pattern!
        #if self.registers[check_index] != cpy:
        #    self._pp()

        self.ip = self.registers[self.ip_index]
        self.ip += 1


    def run(self):

        while True:
            if self.ip >= len(self.commands):
                break
            self._apply_opcode(*self.commands[self.ip])

        return self.registers[0]


def run_decompiled(a):
    c = d = e = f = 0

    c = (c+2)*(c+2)*19*11 + (e+7)*22 + 13
    if a != 0:
        c += (27*28+29)*30*14*32
        return c

    a = 0
    d = 1
    f = 1
    while True:
        # d is a devisor of c
        # so in the end, we are adding up all devisors of c.
        # This is verified by part 1 of this day.
        if d*f == c:
            a += d
        f += 1
        if f > c:
            d += 1
            if d > c:
                print(a)
                return
            f = 1


def main():

    lines = open_data("19.data")

    ip = int(lines[0].split(" ")[1])
    commands = lmap(lambda x: x.split(" "), lines[1:])
    commands = [(c[0], *lmap(int, c[1:])) for c in commands]

    # This works for the first part as well. But takes 6s instead of 0.5s.
    # The decompiled version is just nicer...
    #vm = VM(ip, [0,0,0,0,0,0], commands)
    #print(vm.run())

    run_decompiled(0)

    number = run_decompiled(1)
    # add 1 and number itself as they are ommited from thie prime_factors function...
    print(sum(prime_factors(number))+1+number)


if __name__ == "__main__":
    main()

# year 2018
# solution for 19.01: 1080
# solution for 19.02: 11106760
