from fractions import gcd
import math

def diff(a0, a1):
    return (a1[0]-a0[0], a1[1]-a0[1])

def div(a, f):
    return (a[0]//f if f else 0, a[1]//f if f else 0)

def unique_step(a0, a1):
    return div(diff(a0, a1), abs(gcd(*diff(a0, a1))))

def unique_asteroid_dirs(a0, asteroids):
    s = {unique_step(a0, a) for a in asteroids}
    if (0,0) in s:
        s.remove((0,0))
    return s

# finds the first asteroid from a0 in the direction d
def find_asteroid(a0, a, d, asteroids):
    if a0 != a and a in asteroids:
        return a
    return find_asteroid(a0, (a[0]+d[0],a[1]+d[1]), d, asteroids)

def polar_angle(b):
    angle = math.atan2(b[0], -b[1])
    return angle if b[0] >= 0 else 2*math.pi+angle


if __name__ == "__main__":

    with open("10.data", "r") as f:

        data = f.read().splitlines()

        all_asteroids = [(x,y) for y,l in enumerate(data) for x, a in enumerate(list(l)) if a == "#"]
        unique_asteroids = [unique_asteroid_dirs(asteroid, all_asteroids) for asteroid in all_asteroids]
        # solution for puzzle 1:
        print(max(map(len, unique_asteroids)))

        largest_index = max([(i, len(x)) for i,x in enumerate(unique_asteroids)], key=lambda x:x[1])
        center = all_asteroids[largest_index[0]]

        first_round = unique_asteroid_dirs(center, all_asteroids)
        sorted_round = sorted(first_round, key=polar_angle)
        lasered_astroids = [find_asteroid(center, center, d, all_asteroids) for d in sorted_round]
        # solution for puzzle 2:
        print(lasered_astroids[199][0]*100+lasered_astroids[199][1])

# solution for 10.01: 347
# solution for 10.02: 829
