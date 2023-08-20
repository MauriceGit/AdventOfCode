#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

# i is for the current command index
# _ is for a value we don't need the result of
index = {c:i for i,c in enumerate("abcdi_")}


def num(regs, a):
    try:
        return int(a)
    except ValueError:
        return regs[index[a]]


def toggle(regs, commands, lines, offset):
    i = regs[index["i"]] + num(regs, offset)
    if i < 0 or i >= len(commands):
        return 0
    c = lines[i].split(" ")
    match commands[i][-1]:
        case "cpy":
            commands[i] = ("i", lambda regs, a, b: num(regs, "i") if num(regs, a) == 0 else num(regs, "i")+num(regs, b)-1, c[1:], "jnz")
        case "inc":
            commands[i] = (c[1], lambda regs, a: num(regs, a)-1, c[1:], "dec")
        case "dec":
            commands[i] = (c[1], lambda regs, a: num(regs, a)+1, c[1:], "inc")
        case "jnz":
            commands[i] = (c[2], lambda regs, a, b: num(regs, a), c[1:], "cpy")
        case "tgl":
            commands[i] = (c[1], lambda regs, a: num(regs, a)+1, c[1:], "inc")
    return 0


def interpreter(lines):

    commands = []
    for l in lines:
        if l == "":
            commands.append(("_", lambda regs: 0, [], "nothing"))
            continue
        c = l.split(" ")
        match c[0]:
            case "cpy": commands.append((c[2], lambda regs, a, b: num(regs, a), c[1:], "cpy"))
            case "inc": commands.append((c[1], lambda regs, a: num(regs, a)+1, c[1:], "inc"))
            case "dec": commands.append((c[1], lambda regs, a: num(regs, a)-1, c[1:], "dec"))
            case "jnz": commands.append(("i", lambda regs, a, b: num(regs, "i") if num(regs, a) == 0 else num(regs, "i")+num(regs, b)-1, c[1:], "jnz"))
            case "tgl": commands.append(("_", toggle, [commands, lines, c[1]], "tgl"))
            case "mul": commands.append((c[1], lambda regs, a, b: num(regs, a)*num(regs, b), c[2:], "mul"))
            case "add": commands.append((c[1], lambda regs, a, b: num(regs, a)+num(regs, b), c[1:], "add"))

    for reg_0 in [7, 12]:
        regs = [0 for c in "abcdi_"]
        regs[0] = reg_0
        _commands = deepcopy(commands)

        while regs[index["i"]] < len(_commands):
            target, f, args, f_type = _commands[regs[index["i"]]]
            regs[index[target]] = f(regs, *args)
            regs[index["i"]] += 1

        print(regs[0])


def main():

    lines = open_data("23.data", no_filter=True)

    interpreter(lines)


if __name__ == "__main__":
    main()

# year 2016
# solution for 23.01: 14445
# solution for 23.02: 479011005
