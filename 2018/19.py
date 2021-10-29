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
    ops = [
        lambda r,a,b: r[a] + r[b],      # addr
        lambda r,a,b: r[a] + b,                      # addi
        lambda r,a,b: r[a] * r[b],      # mulr
        lambda r,a,b: r[a] * b,                      # muli
        lambda r,a,b: r[a] & r[b],      # banr
        lambda r,a,b: r[a] & b,                      # bani
        lambda r,a,b: r[a] | r[b],      # borr
        lambda r,a,b: r[a] | b,                      # bori
        lambda r,a,b: r[a],                          # setr
        lambda r,a,b: a,                                          # seti
        lambda r,a,b: int(a > r[b]),                 # gtir
        lambda r,a,b: int(r[a] > b),                 # gtri
        lambda r,a,b: int(r[a] > r[b]), # gtrr
        lambda r,a,b: int(a == r[b]),                # eqir
        lambda r,a,b: int(r[a] == b),                # eqri
        lambda r,a,b: int(r[a] == r[b]),# eqrr
    ]


    def __init__(self, ip_index, registers, commands):
        self.registers = registers[:]
        self.commands = [(self.command_dict[c[0]], *c[1:]) for c in commands]
        self.ip_index = ip_index


    def _apply_opcode(self, opcode, a, b, c):

        self.registers[self.ip_index] = self.ip

        self.registers[c] = self.ops[opcode](self.registers, a, b)

        self.ip = self.registers[self.ip_index]
        self.ip += 1


    def run(self):

        while True:
            if self.ip >= len(self.commands):
                break
            self._apply_opcode(*self.commands[self.ip])
            #print(self.registers[0])

        return self.registers[0]


def main():

    lines = open_data("19.data")

    ip = int(lines[0].split(" ")[1])
    commands = lmap(lambda x: x.split(" "), lines[1:])
    commands = [(c[0], *lmap(int, c[1:])) for c in commands]

    vm = VM(ip, [0]*6, commands)
    print(vm.run())

    #vm = VM(ip, [1,0,0,0,0,0], commands)
    #print(vm.run())



if __name__ == "__main__":
    main()

# year 2018
# solution for 19.01: 1080
# solution for 19.02:
