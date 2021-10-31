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


def main():

    lines = open_data("19.data")

    ip = int(lines[0].split(" ")[1])
    commands = lmap(lambda x: x.split(" "), lines[1:])
    commands = [(c[0], *lmap(int, c[1:])) for c in commands]

    vm = VM(ip, [0,0,0,0,0,0], commands)
    print(vm.run())

    # Took a long time to solve this one. Didn't do it without some help from reddit:
    # https://old.reddit.com/r/adventofcode/comments/a7j9zc/2018_day_19_solutions/ec40xhf/
    #
    # The solution was, to look at how the registers and see how they look, when registers[0] changes!
    # Then the numbers in column 4 look like prime factors of the numbers in column 3.
    # Then it is easy to see, that column 0 just adds up the prime-factors from column 4.
    # Therefore the easiest way to calculate the final result (what should be in column 1 at the end)
    # by taking the number in column 3 --> 10551403 and using wolfram-alpha to calculate the prime-factors:
    # [1, 19, 555337, 10551403] and adding them all up: 11106760. This is the final result!
    #
    # I tried translating the "assembly" into some higher-level form first but got hung up on
    # the jumping/goto part of it. It took way too much time, annoyed me and I looked at the completely
    # wrong parts of the code (loop indices, ...) and had a hard time to figure out, what exactly was
    # happening here.
    # As it isn't even christmas and I am doing it for fun, I had a look at some answers until it made more sense...


if __name__ == "__main__":
    main()

# year 2018
# solution for 19.01: 1080
# solution for 19.02: 11106760
