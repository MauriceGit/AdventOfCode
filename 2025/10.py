#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *
import pulp


Machine = recordtype("Machine", "result length buttons joltage")


def press_p1(lights, button, result_length):
    for b in button:
        lights ^= 1 << ((result_length-1)-b)
    return lights

def press_button_p1(machine):

    queue = [(0, 0)]
    visited = set()

    while True:
        count, lights = heappop(queue)
        if lights == machine.result:
            return count
        if lights in visited:
            continue
        visited.add(lights)

        for button in machine.buttons:
            heappush(queue, (count+1, press_p1(lights, button, machine.length)))


def solve_with_solver(m):

    # Define problem: minimize the overall button clicks
    prob = pulp.LpProblem("MinimizeSum", pulp.LpMinimize)

    # A variable for each button. Can not be negative and needs to be an integer.
    variables = [pulp.LpVariable(str(i), lowBound=0, cat='Integer') for i in range(len(m.buttons))]

    # Objective - this is the main thing. We want to minimize the overall
    # button clicking. So the sum of all buttons need to be minimized.
    prob += sum(variables)

    # Add the equations
    for i, joltage in enumerate(m.joltage):
        prob += sum(variables[bi] for bi, b in enumerate(m.buttons) if i in b) == joltage

    # Solve
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    return int(sum([v.value() for v in variables]))


def main():

    lines = open_data("10.data")
    machines = []
    for line in lines:
        res_str = line[1:].split("]")[0]
        result = int("".join(map(lambda x: "1" if x=="#" else "0", res_str)), 2)
        buttons = lmap(ints, line.split("] (")[1].split(") {")[0].split(") ("))
        joltage = ints(line[:-1].split(" {")[1])
        machines.append(Machine(result, len(res_str), buttons, joltage))

    print(sum(press_button_p1(m) for m in machines))

    print(sum(solve_with_solver(m) for m in machines))


if __name__ == "__main__":
    main()

# year 2025
# solution for 10.01: 399
# solution for 10.02: 15631
