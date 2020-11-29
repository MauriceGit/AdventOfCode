from collections import defaultdict


def find_target(visited, node, target):

    if node == target:
        return True, 0

    if node in visited:
        return False, 0
    visited[node] = True

    for k in orbited[node]:
        found, cnt = find_target(visited, k, target)
        if found:
            return True, cnt+1

    if node in orbiting:
        found, cnt = find_target(visited, orbiting[node], target)
        if found:
            return True, cnt+1

    return False, 0

def calc_dist(source, target):
    visited = dict()
    return find_target(visited, source, target)[1]


# with list of orbits around myself
orbiting = defaultdict(str)
orbited  = defaultdict(list)

if __name__ == "__main__":

    with open("06.data", "r") as f:

        for o in f.read().splitlines():
            center, orbit = o.split(")")[:2]
            orbiting[orbit] = center
            orbited[center].append(orbit)

        orbit_count = sum([calc_dist(k, "COM") for k in orbiting])

        # first puzzle
        print(orbit_count)
        # second puzzle
        print(calc_dist("YOU", "SAN")-2)

# solution for 06.01: 292387
# solution for 06.02: 433
