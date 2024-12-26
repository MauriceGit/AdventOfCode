#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

import matplotlib.pyplot as plt

def part1(inputs, ops):
    while len(ops) > 0:
        for k, v in ops.items():
            if k not in inputs and v[1] in inputs and v[2] in inputs:
                inputs[k] = v[0](inputs[v[1]], inputs[v[2]])
                del ops[k]
                break

    return int("".join([str(int(inputs[k])) for k in sorted(filter(lambda x: x.startswith("z"), inputs.keys()), key=lambda x: int(x[1:]), reverse=True)]), 2)


def pp_(inputs, ops, n):

    if n in inputs:
        return f"{n}"

    o, a, b = ops[n]
    op = ""
    match o:
        case operator.and_:
            op = "&"
        case operator.or_:
            op = "|"
        case operator.xor:
            op = "^"

    print(f"{n} = {a} {op} {b}")
    return f"({pp_(inputs, ops, a)} {op} {pp_(inputs, ops, b)})"

def pp(inputs, ops, n):
    print(pp_(inputs, ops, n))


# carryover is the OR leftover from the n-1 operation
def calc_bit_n(ops, ops_or, ops_and, ops_xor, n, carryover):

    wrong_nodes = []

    new_carryover = None

    xn, yn, zn = "x"+n, "y"+n, "z"+n

    xy_xor = ops_xor[(xn, yn)]
    xy_and = ops_and[(xn, yn)]

    # zn is always the xor of the carryover and xn^yn
    op, a, b = ops[zn]
    if op != operator.xor or (a != carryover and b != carryover):
        print(f"wrong: {zn}")
        wrong_nodes.append(zn)
        print(f"({xy_xor}, {carryover})")
        wrong_nodes.append(ops_xor[(xy_xor, carryover)])
        print("Wrong Nodes: ", wrong_nodes)

    def switch(n):
        if n in wrong_nodes:
            return wrong_nodes[0] if n == wrong_nodes[1] else wrong_nodes[1]
        return n


    second_and = switch(ops_and[(carryover, xy_xor)])

    #print(f"second_and: {second_and}")

    new_carryover = switch(ops_or[(second_and, switch(xy_and))])

    #print(f"new carryover: {new_carryover}")

    return new_carryover, wrong_nodes




    and_ = ops_and[("x"+n, "y"+n)]
    xor_ = ops_xor[("x"+n, "y"+n)]

    # this should result in zn
    zn = ops_xor[(carryover, xor_)]
    #print(zn)

    and2_ = ops_and[(carryover, xor_)]

    # this is the new carryover for n+1
    or_ = ops_or[(and_, and2_)]

    return or_, []


def calc_bits(ops, ops_or, ops_and, ops_xor):

    carryover = ops_and[("x00", "y00")]
    for i in range(1, 46):
        n = f"{i:02d}"

        carryover, _ = calc_bit_n(ops, ops_or, ops_and, ops_xor, n, carryover)





def main():

    lines = open_data_groups("24.data")

    G = nx.Graph()

    inputs = dict()
    for l in lines[0]:
        i, b = l.split(": ")
        inputs[i] = b == "1"

    # result <- (op-function, input1, input2)
    ops = dict()
    # (a,b) --> result of AND
    ops_and = dict()
    ops_or = dict()
    ops_xor = dict()
    for l in lines[1]:
        ab, res = l.split(" -> ")
        a, op, b = ab.split(" ")
        o = {"AND": operator.and_, "OR": operator.or_, "XOR": operator.xor}[op]
        ops[res] = (o, a, b)

        match op:
            case "AND":
                ops_and[(a,b)] = res
                ops_and[(b,a)] = res
            case "OR":
                ops_or[(a,b)] = res
                ops_or[(b,a)] = res
            case "XOR":
                ops_xor[(a,b)] = res
                ops_xor[(b,a)] = res

        c = {"AND": "r", "OR": "b", "XOR": "g"}[op]
        G.add_edge(a, res, color=c)
        G.add_edge(b, res, color=c)

    print(part1(inputs.copy(), ops.copy()))

    #pp(inputs, ops, "z00")
    #pp(inputs, ops, "z01")
    #pp(inputs, ops, "z02")
    #pp(inputs, ops, "z03")


    #calc_bit_n(inputs, ops, ops_or, ops_and, ops_xor, 1, None)
    calc_bits(ops, ops_or, ops_and, ops_xor)

    if False:
        colors = nx.get_edge_attributes(G,'color').values()

        pos = nx.kamada_kawai_layout(G)
        nx.draw(G, pos,
                edge_color=colors,
                with_labels=True,
                node_color='lightgreen')

        plt.show()


if __name__ == "__main__":
    main()

# year 2024
# solution for 24.01: ?
# solution for 24.02: ?
