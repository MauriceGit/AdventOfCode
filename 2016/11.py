#!/usr/bin/env python3

import sys
sys.path.append('../General')
from utility import *

chip_count = 0
bit_positions = [np.uint64(2**p) for p in range(64)]
mc1_pattern = np.uint64(0)

def print_bits(floors):
    print(format(floors, "#0{}b".format(4*chip_count*2+4))[2:])

def print_floors(floors):
    all_fmt = ""
    for floor in range(4):
        fmt = ""
        for gen in range(chip_count):
            fmt = ("G" if has_gen(floors, gen, floor) else "-") + fmt
        fmt = "|" + fmt
        for chip in range(chip_count):
            fmt = ("C" if has_chip(floors, chip, floor) else "-") + fmt
        fmt = ("X" if has_elevator(floors, floor) else "-") + "|" + fmt
        all_fmt = f"Floor {floor}: " + fmt + "\n" + all_fmt
    print(all_fmt)

# Bits
def set_bit(floors, position):
    return floors | bit_positions[position]
def unset_bit(floors, position):
    return floors & ~bit_positions[position]
def has_bit(floors, position):
    return floors & bit_positions[position] != 0

# Generators
def set_gen(floors, gen, floor):
    return set_bit(floors, floor*chip_count*2 + gen)
def unset_gen(floors, gen, floor):
    return unset_bit(floors, floor*chip_count*2 + gen)
def has_gen(floors, gen, floor):
    return has_bit(floors, floor*chip_count*2 + gen)
def move_gen(floors, gen, source, dest):
    tmp = unset_gen(floors, gen, source)
    return set_gen(tmp, gen, dest)

# Microchips
def set_chip(floors, chip, floor):
    return set_gen(floors, chip+chip_count, floor)
def unset_chip(floors, chip, floor):
    return unset_gen(floors, chip+chip_count, floor)
def has_chip(floors, chip, floor):
    return has_gen(floors, chip+chip_count, floor)
def move_chip(floors, chip, source, dest):
    return set_chip(unset_chip(floors, chip, source), chip, dest)

# Elevator
def set_elevator(floors, floor):
    return set_bit(floors, 4*chip_count*2+floor)
def unset_elevator(floors, floor):
    return unset_bit(floors, 4*chip_count*2 + floor)
def has_elevator(floors, floor):
    return has_bit(floors, 4*chip_count*2 + floor)
def move_elevator(floors, source, dest):
    return set_elevator(unset_elevator(floors, source), dest)

def chip_fries(floors, chip, level):
    if has_gen(floors, chip, level):
        return False
    # If there are any generators, the chip will fry!
    return floors & ((np.uint64(2**(chip_count)-1))<<np.uint64((chip_count*2*level))) != 0


def all_chips_ok(floors):
    for l in range(4):
        for c in range(chip_count):
            if has_chip(floors, c, l) and chip_fries(floors, c, l):
                return False
    return True

def current_floor(floors):
    for i in range(4):
        if has_elevator(floors, i):
            return i
    return -1

def gen_on_floor(floors, floor):
    for g in range(chip_count):
        if has_gen(floors, g, floor):
            yield g

def chips_on_floor(floors, floor):
    for c in range(chip_count):
        if has_chip(floors, c, floor):
            yield c


def visit(state, pos, dist, path):
    # all first three floors are empty - We finished!
    return pos & np.uint64(2**(3*chip_count*2)-1) != 0


def chips_on_floor_ok(floors, floor):
    for c in range(chip_count):
        if has_chip(floors, c, floor) and chip_fries(floors, c, floor):
            return False
    return True

def get_neighbors(floors):

    floor = current_floor(floors)
    offset = [f for f in [-1, 1] if floor+f >= 0 and floor+f <= 3]

    neighbors = []

    for off in offset:
        new_floor = move_elevator(floors, floor, floor+off)

        for c1 in chips_on_floor(new_floor, floor):

            # Move one Microchip and one Generator
            # Can only move with its own Generator because the chip would fry on this or the next floor!
            if has_gen(new_floor, c1, floor):
                move_c1_g1 = move_gen(move_chip(new_floor, c1, floor, floor+off), c1, floor, floor+off)
                if chips_on_floor_ok(move_c1_g1, floor+off):
                    neighbors.append(move_c1_g1)

            move_c1 = move_chip(new_floor, c1, floor, floor+off)

            if chip_fries(move_c1, c1, floor+off):
                continue

            for c2 in chips_on_floor(move_c1, floor):
                move_c1_c2 = move_chip(move_c1, c2, floor, floor+off)
                if c1 != c2 and not chip_fries(move_c1_c2, c2, floor+off):
                    # Move two Microchips
                    neighbors.append(move_c1_c2)

            # Move only one Microchip
            neighbors.append(move_c1)

        for g1 in gen_on_floor(new_floor, floor):

            # Move only one Generator
            move_g1 = move_gen(new_floor, g1, floor, floor+off)

            for g2 in gen_on_floor(move_g1, floor):
                if g1 != g2:
                    move_g2 = move_gen(move_g1, g2, floor, floor+off)
                    if chips_on_floor_ok(move_g2, floor+off) and chips_on_floor_ok(move_g2, floor):
                        # Move two Generators
                        neighbors.append(move_g2)

            if chips_on_floor_ok(move_g1, floor+off) and chips_on_floor_ok(move_g1, floor):
                neighbors.append(move_g1)

    return neighbors

# mirror every microchip-generator with every other pair. No pair is in any way different logically,
# so it doesn't matter if pairs are mirrored. Only that they all end up on level 4.
def calc_mirror_states(floors):
    mirrors = set()

    for c1 in range(chip_count):
        for c2 in range(c1+1, chip_count):
            offset = np.uint64(c2-c1)
            # contains only two bits. One bit with the location of the microchip and another bit with the location of
            # the corresponding generator
            mc1_mask = floors & (mc1_pattern<<np.uint64(c1))
            mc2_mask = floors & (mc1_pattern<<np.uint64(c2))

            # set bits from both masks to 0
            # set bits from the two masks on the mirrored position!
            exchanged = (floors & ~mc1_mask & ~mc2_mask) | mc1_mask<<np.uint64(offset) | mc2_mask>>np.uint64(offset)

            mirrors.add(exchanged)

    return mirrors


def run(floors):
    global mc1_pattern
    # first Microchip/Generator pattern for all levels
    cc = chip_count
    mc1_pattern = np.uint64(1 | 1<<cc | 1<<(2*cc) | 1<<(3*cc) | 1<<(4*cc) | 1<<(5*cc) | 1<<(6*cc) | 1<<(7*cc))

    end_pos = np.uint64(2**(chip_count*2)-1) << np.uint64(3*chip_count*2)
    end_pos = set_elevator(end_pos, 3)

    queue = [(0, floors)]
    heapify(queue)
    visited = set()

    while len(queue) > 0:

        steps, state = heappop(queue)

        if state in visited:
            continue

        if state == end_pos:
            return steps

        visited.add(state)
        visited |= calc_mirror_states(state)

        for n in get_neighbors(state):
            heappush(queue, (steps+1, n))

    return -1

def run_input(lines):
    # The general layout is one 64bit integer with bits set for each microchip and generator.
    # starting from the right with floor 0. With 2 chips we have 4 bits per level. With 4 levels.
    # then an additional 4 bits where the elevator currently is. All in all:
    # 20bits: (#chips + #generators) * #floors + #floors
    floors = np.uint64(0)

    indices = dict()
    index = 0

    microchips = []
    generators = []

    for i,line in enumerate(lines):
        for g in re.finditer(r"(\w+-compatible microchip)", line):
            chip = g.group(0).split("-")[0]
            if chip not in indices:
                indices[chip] = index
                index += 1
            microchips.append((indices[chip], i))
        for g in re.finditer(r"(\w+ generator)", line):
            gen = g.group(0).split(" ")[0]
            if gen not in indices:
                indices[gen] = index
                index += 1
            generators.append((indices[gen], i))

    global chip_count
    chip_count = index

    floors = set_elevator(floors, 0)

    for (chip, level) in microchips:
        floors = set_chip(floors, chip, level)
    for (gen, level) in generators:
        floors = set_gen(floors, gen, level)

    return run(floors)

def main():

    lines = open_data("11.data")
    print(run_input(lines))

    lines[0] += "An elerium generator."
    lines[0] += "An elerium-compatible microchip."
    lines[0] += "A dilithium generator"
    lines[0] += "A dilithium-compatible microchip."
    print(run_input(lines))


if __name__ == "__main__":
    main()

# year 2016
# solution for 11.01: 33
# solution for 11.02: 57
