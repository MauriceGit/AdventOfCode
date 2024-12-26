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


def switch1(a):
    return a

# Nodes we know: xn, yn, zn, carryover. xn, yn and carryover are known to be good!
# We need 4 more nodes!
# Returns: (nodes, new_carryover, everything_ok)
# new_carryover can be wrong, if everything_ok is False.
def test_bit_n(ops, ops_or, ops_and, ops_xor, n, carryover, switch=switch1):
    xn, yn, zn = "x"+n, "y"+n, "z"+n

    xy_xor = switch(ops_xor[(xn, yn)])
    xy_and = switch(ops_and[(xn, yn)])

    op, a, b = ops[switch(zn)]
    if op != operator.xor or carryover not in (a, b) or xy_xor not in (a, b):
        return None, False

    if (carryover, xy_xor) not in ops_and:
        return None, False

    second_and = switch(ops_and[(carryover, xy_xor)])

    if (xy_and, second_and) not in ops_or:
        return None, False

    return switch(ops_or[(xy_and, second_and)]), True

# We can go 2 levels deep and collect EVERY node. That should get us all relevant nodes...
def collect_nodes(ops, ops_or, ops_and, ops_xor, n, carryover):
    xn, yn, zn = "x"+n, "y"+n, "z"+n
    nodes = {xn, yn}

    xy_xor = ops_xor[(xn, yn)]
    xy_and = ops_and[(xn, yn)]
    nodes.add(xy_xor)
    nodes.add(xy_and)

    l1_nodes = set()

    for op in (ops_or, ops_and, ops_xor):
        if (xy_xor, carryover) in op:
            node = op[(xy_xor, carryover)]
            nodes.add(node)
            l1_nodes.add(node)

    for op in (ops_or, ops_and, ops_xor):
        for next_node in l1_nodes:
            if (next_node, xy_and) in op:
                nodes.add(op[(next_node, xy_and)])
    return nodes


def calc_bits(ops, ops_or, ops_and, ops_xor):
    wrong_nodes = []
    carryover = ops_and[("x00", "y00")]
    for i in range(1, 48):
        n = f"{i:02d}"
        xn, yn = "x"+n, "y"+n

        if (xn, yn) not in ops_xor:
            break

        nodes = collect_nodes(ops, ops_or, ops_and, ops_xor, n, carryover)
        new_carryover, ok = test_bit_n(ops, ops_or, ops_and, ops_xor, n, carryover)
        if not ok:
            for (a,b) in combinations(nodes - {xn, yn}, 2):
                switch2 = lambda x: x if x not in (a, b) else (a if x==b else b)
                new_carryover, ok = test_bit_n(ops, ops_or, ops_and, ops_xor, n, carryover, switch=switch2)
                if ok:
                    carryover = new_carryover
                    wrong_nodes.extend([a, b])
                    break
        else:
            carryover = new_carryover

    return ",".join(sorted(wrong_nodes))


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

        _ops = {"AND": ops_and, "OR": ops_or, "XOR": ops_xor}[op]
        _ops[(a,b)] = res
        _ops[(b,a)] = res

        if False:
            c = {"AND": "r", "OR": "b", "XOR": "g"}[op]
            G.add_edge(a, res, color=c)
            G.add_edge(b, res, color=c)

    print(part1(inputs.copy(), ops.copy()))

    print(calc_bits(ops, ops_or, ops_and, ops_xor))

    # Draw the graph to get an initial overview of node structure!
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
# solution for 24.01: 59619940979346
# solution for 24.02: bpt,fkp,krj,mfm,ngr,z06,z11,z31
