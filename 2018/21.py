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
        lambda r,a,b: r[a] + r[b], # addr
        lambda r,a,b: r[a] + b,    # addi
        lambda r,a,b: r[a] * r[b], # mulr
        lambda r,a,b: r[a] * b,    # muli
        lambda r,a,b: r[a] & r[b], # banr
        lambda r,a,b: r[a] & b,    # bani
        lambda r,a,b: r[a] | r[b], # borr
        lambda r,a,b: r[a] | b,    # bori
        lambda r,a,b: r[a],        # setr
        lambda r,a,b: a,           # seti
        lambda r,a,b: a > r[b],    # gtir
        lambda r,a,b: r[a] > b,    # gtri
        lambda r,a,b: r[a] > r[b], # gtrr
        lambda r,a,b: a == r[b],   # eqir
        lambda r,a,b: r[a] == b,   # eqri
        lambda r,a,b: r[a] == r[b],# eqrr
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

    # a and b are indices
    def __pp_reg(self, cc, a, b, c):
        if c == a or c == b:
            print(f"regs[{c}] {cc}= {b if a == c else a}")
        else:
            print(f"regs[{c}] = regs[{a}] {cc} regs[{b}]")

    # b is used as value, not index!
    def __pp_val(self, cc, a, b, c):
        if c == a:
            print(f"regs[{c}] {cc}= {b}")
        else:
            print(f"regs[{c}] = regs[{a}] {cc} {b}")


    def _pp_command(self, opcode, a, b, c):

        if opcode == 0:
            self.__pp_reg("+", a, b, c)
        if opcode == 1:
            self.__pp_val("+", a, b, c)
        if opcode == 2:
            self.__pp_reg("*", a, b, c)
        if opcode == 3:
            self.__pp_val("*", a, b, c)
        if opcode == 4:
            self.__pp_reg("&", a, b, c)
        if opcode == 5:
            self.__pp_val("&", a, b, c)
        if opcode == 6:
            self.__pp_reg("|", a, b, c)
        if opcode == 7:
            self.__pp_val("|", a, b, c)
        if opcode == 8:
            print(f"regs[{c}] = regs[{a}]")
        if opcode == 9:
            print(f"regs[{c}] = {a}")
        if opcode == 10:
            print(f"regs[{c}] = {a} > regs[{b}]")
        if opcode == 11:
            print(f"regs[{c}] = regs[{a}] > {b}")
        if opcode == 12:
            print(f"regs[{c}] = regs[{a}] > regs[{b}]")
        if opcode == 13:
            print(f"regs[{c}] = {a} == regs[{b}]")
        if opcode == 14:
            print(f"regs[{c}] = regs[{a}] == {b}")
        if opcode == 15:
            print(f"regs[{c}] = regs[{a}] == regs[{b}]")




    def _apply_opcode(self, opcode, a, b, c):

        self.registers[self.ip_index] = self.ip
        last_ip = self.ip
        #check_index = 5
        #cpy = self.registers[check_index]

        #print(f"{str(self.ip).ljust(2)}: ", end="")
        #self._pp_command(opcode, a, b, c)

        self.registers[c] = int(self.ops[opcode](self.registers, int(a), int(b)))

        # Uncomment to see the output that made it easy to see the pattern!
        #if self.registers[check_index] != cpy:
        #    self._pp()

        self.ip = self.registers[self.ip_index]
        self.ip += 1
        #if self.ip != last_ip+1:
        #    print(f"goto {self.ip}")


    def run(self):

        while True:
        #for i in range(100):
            if self.ip >= len(self.commands):
                break
            self._apply_opcode(*self.commands[self.ip])

        return self.registers[0]


def main():

    lines = open_data("21.data")

    ip = int(lines[0].split(" ")[1])
    commands = lmap(lambda x: x.split(" "), lines[1:])
    commands = [(c[0], *lmap(int, c[1:])) for c in commands]

    vm = VM(ip, [214,0,0,0,0,0], commands)
    print(vm.run())


if __name__ == "__main__":
    main()

# year 2018
# solution for 21.01: ?
# solution for 21.02: ?
