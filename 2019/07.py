from collections import defaultdict
import itertools
from intcode import IntCode

def try_combination(phase, instruction, max_iterations):
    next_input = 0

    amplifiers = [IntCode(instruction[:]) for i in range(len(phase))]

    first_round = True
    iteration = 1

    while True:
        if max_iterations!= -1 and iteration > max_iterations:
            break

        for i, amplifier in enumerate(amplifiers):

            if first_round:
                new_inputs = [phase[i], next_input]
            else:
                new_inputs = [next_input]

            amplifier.set_inputs(new_inputs)
            output = amplifier.get_outputs()[-1]

            if i == len(phase)-1 and amplifier.is_finished():
                return amplifier.get_all_outputs()[-1]

            next_input = output

        first_round = False
        iteration += 1

    return 0


if __name__ == "__main__":

    instruction = [3,8,1001,8,10,8,105,1,0,0,21,30,55,80,101,118,199,280,361,442,99999,3,9,101,4,9,9,4,9,99,3,9,101,4,9,9,1002,9,4,9,101,4,9,9,1002,9,5,9,1001,9,2,9,4,9,99,3,9,101,5,9,9,1002,9,2,9,101,3,9,9,102,4,9,9,1001,9,2,9,4,9,99,3,9,102,2,9,9,101,5,9,9,102,3,9,9,101,3,9,9,4,9,99,3,9,1001,9,2,9,102,4,9,9,1001,9,3,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,99]
    # puzzle 1 test:
    #instruction = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    #instruction = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
    #instruction = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
    # puzzle 2 test:
    #instruction = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    #instruction = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]

    phase_puzzle_0 = [0,1,2,3,4]
    phase_puzzle_1 = [5,6,7,8,9]

    puzzle1_output = 0
    for phase in itertools.permutations(phase_puzzle_0):
        puzzle1_output = max(puzzle1_output, try_combination(phase, instruction, 1))
        #break
    print(puzzle1_output)

    puzzle2_output = 0
    for phase in itertools.permutations(phase_puzzle_1):
        puzzle2_output = max(puzzle2_output, try_combination(phase, instruction, -1))
    print(puzzle2_output)

# solution for 07.01: 43812
# solution for 07.02: 59597414
