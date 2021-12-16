#!/usr/bin/env python3.7

import sys
sys.path.append('../General')
from utility import *
from operator import mul

# returns (version, type_id, number), read_bit_length
def parse_packet(bits, i):

    version = int(bits[i:i+3], 2)
    type_id = int(bits[i+3:i+6], 2)
    i += 6
    # literal value
    value = ""
    if type_id == 4:
        while True:
            next_four = bits[i:i+5]
            i += 5
            value += next_four[1:]
            if next_four[0] == "0":
                break
        return (version, type_id, int(value, 2)), i


    length_type_id = int(bits[i], 2)
    i += 1
    tmp = 15 if length_type_id == 0 else 11
    number = int(bits[i:i+tmp], 2)
    i += tmp

    packets = []
    if length_type_id == 0:
        # number of bits
        tmp_i = i
        while True:
            packet, tmp_i = parse_packet(bits, tmp_i)
            packets.append(packet)
            if tmp_i-i >= number:
                break
        i = tmp_i

    else:
        # number of packets
        for j in range(number):
            packet, i = parse_packet(bits, i)
            packets.append(packet)


    return (version, type_id, packets), i

def parse(bits):
    i = 0
    end = False
    packets = []
    while not end:
        if int(bits[i:], 2) == 0:
            break

        packet, i = parse_packet(bits, i)

        packets.append(packet)

    return packets



def part_1(packets):

    s = 0
    for p in packets:
        s += p[0]
        if p[1] != 4:
            s += part_1(p[2])
    return s

def evaluate(packets):
    res = 0
    for p in packets:

        if p[1] == 4:
            res = p[2]
        else:
            sub_packets = [evaluate([tmp_p]) for tmp_p in p[2]]

            if p[1] == 0:
                res = sum(sub_packets)
            elif p[1] == 1:
                res = reduce(mul, sub_packets)
            elif p[1] == 2:
                res = min(sub_packets)
            elif p[1] == 5:
                res = int(sub_packets[0] > sub_packets[1])
            elif p[1] == 6:
                res = int(sub_packets[0] < sub_packets[1])
            elif p[1] == 7:
                res = int(sub_packets[0] == sub_packets[1])


    return res



def main():

    lines = open_data("16.data")

    bits = ""

    i = 0
    while i < len(lines[0]):
        bits += bin(int(lines[0][i], 16))[2:].zfill(4)
        i += 1

    packets = parse(bits)

    print(part_1(packets))

    print(packets)
    print(evaluate(packets))




if __name__ == "__main__":
    main()

# year 2021
# solution for 16.01: ?
# solution for 16.02: ?
