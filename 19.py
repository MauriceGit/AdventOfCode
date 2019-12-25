from intcode import IntCode
from utility import draw
from collections import defaultdict, Counter


def try_beam_count(y):
    dx = 0
    dy = y
    last_value = 0
    beam_cnt = 0

    while True:
        machine = IntCode(data)
        machine.set_inputs([dx, dy])
        beam = machine.get_outputs()[0]

        if beam == 0 and last_value == 1:
            return first_x, dy+1, beam_cnt
        if beam == 1 and last_value == 0:
            first_x = dx

        beam_cnt += beam
        last_value = beam
        dx += 1
        dy -= 1
    return 0,0,0





if __name__ == "__main__":

    data = [109,424,203,1,21101,11,0,0,1106,0,282,21102,18,1,0,1106,0,259,1201,1,0,221,203,1,21102,31,1,0,1106,0,282,21101,0,38,0,1105,1,259,21002,23,1,2,21202,1,1,3,21102,1,1,1,21102,1,57,0,1105,1,303,2101,0,1,222,21002,221,1,3,21002,221,1,2,21101,0,259,1,21101,0,80,0,1105,1,225,21101,169,0,2,21101,0,91,0,1106,0,303,1202,1,1,223,20101,0,222,4,21101,259,0,3,21102,225,1,2,21102,225,1,1,21101,0,118,0,1106,0,225,20102,1,222,3,21101,94,0,2,21101,0,133,0,1106,0,303,21202,1,-1,1,22001,223,1,1,21102,148,1,0,1105,1,259,2102,1,1,223,21001,221,0,4,21002,222,1,3,21101,0,22,2,1001,132,-2,224,1002,224,2,224,1001,224,3,224,1002,132,-1,132,1,224,132,224,21001,224,1,1,21101,0,195,0,106,0,108,20207,1,223,2,21002,23,1,1,21102,1,-1,3,21102,214,1,0,1105,1,303,22101,1,1,1,204,1,99,0,0,0,0,109,5,1202,-4,1,249,21201,-3,0,1,21202,-2,1,2,22101,0,-1,3,21101,0,250,0,1106,0,225,21202,1,1,-4,109,-5,2106,0,0,109,3,22107,0,-2,-1,21202,-1,2,-1,21201,-1,-1,-1,22202,-1,-2,-2,109,-3,2105,1,0,109,3,21207,-2,0,-1,1206,-1,294,104,0,99,21202,-2,1,-2,109,-3,2105,1,0,109,5,22207,-3,-4,-1,1206,-1,346,22201,-4,-3,-4,21202,-3,-1,-1,22201,-4,-1,2,21202,2,-1,-1,22201,-4,-1,1,22101,0,-2,3,21102,343,1,0,1105,1,303,1106,0,415,22207,-2,-3,-1,1206,-1,387,22201,-3,-2,-3,21202,-2,-1,-1,22201,-3,-1,3,21202,3,-1,-1,22201,-3,-1,2,21201,-4,0,1,21101,0,384,0,1105,1,303,1106,0,415,21202,-4,-1,-4,22201,-4,-3,-4,22202,-3,-2,-2,22202,-2,-4,-4,22202,-3,-2,-3,21202,-4,-1,-2,22201,-3,-2,1,21201,1,0,-4,109,-5,2106,0,0]

    field = defaultdict(int)

    for y in range(50):
        for x in range(50):
            machine = IntCode(data)
            machine.set_inputs([x,y])
            beam = machine.get_outputs()[0]
            field[(x,y)] = beam

    # solution for puzzle 1
    print(sum(field.values()))
    #draw(field)

    x = y = 0
    # just make it kinda large.
    diff = 2000
    while True:
        p_x, p_y, cnt = try_beam_count(y)

        if cnt > 100:
            diff //= 2
            y -= diff
        elif cnt == 100:
            # sometimes the beam gets narrower for a bit. So go back a bit and find the first.
            # 30 steps back is just random really, seems to be enough.
            init_y = y - 30
            cnt = 0
            while cnt < 100:
                p_x, p_y, cnt = try_beam_count(init_y)
                init_y += 1

            # solution for puzzle 2:
            print(p_x*10000+p_y)
            break
        elif cnt < 100:
            y += diff

# solution for 19.01: 160
# solution for 19.02: 9441282
