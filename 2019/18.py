import networkx as nx
from utility import add_p
from collections import defaultdict

def add_edge(graph, p, d):
    if add_p(p, d) in graph:
        graph.add_edge(p, add_p(p, d), weight=1)
    else:
        graph.add_node(p)
def add_surrounding_edge(graph, p):
    add_edge(graph, p, ( 1,0))
    add_edge(graph, p, (-1,0))
    add_edge(graph, p, (0, 1))
    add_edge(graph, p, (0,-1))

def path_length_puzzle_1(node_dist, node_keys, c_to_p, p_to_c):

    # set with all keys
    all_keys = {k for k in c_to_p.keys() if k.lower() == k and k != "@"}

    # (path, score, node, found_keys)
    queue = [([], 0, "@", set())]
    solutions = []

    cache = dict()

    current_best_score = 10000000000000000

    path_cache = dict()
    # if we have been at a specific situation with the same collected keys at a node, we can discard
    # the new path, if the score is higher than one we had before!
    situation_cache = dict()

    def find_paths(node, found_keys):
        remaining_keys = all_keys - found_keys
        for k in remaining_keys:
            # Do I have enough keys, to go to this one?
            if len(node_keys[node][k] - found_keys - {"@"}) == 0:
                yield k


    while len(queue) > 0:

        new_queue = []
        for q in queue:

            path = q[0]
            score = q[1]
            node = q[2]
            found_keys = q[3].union({node})

            if node == "@":
                found_keys = found_keys - {"@"}

            if len(found_keys) == len(all_keys):
                solutions.append((path+[node], score))
                current_best_score = min(current_best_score, score)
                continue

            # early exit, already too slow...
            if score >= current_best_score:
                continue

            node_hash = (node, tuple(found_keys))
            if node_hash in situation_cache:
                if situation_cache[node_hash] <= score:
                    continue

            situation_cache[node_hash] = score

            if node_hash in path_cache:
                all_paths = path_cache[node_hash]
            else:
                all_paths = list(find_paths(node, found_keys))

            if node_hash not in path_cache:
                path_cache[node_hash] = all_paths

            for p in all_paths:
                new_queue.append((path+[node], score+node_dist[node][p], p, found_keys))

        queue = new_queue

    return sorted(solutions, key=lambda x: x[1])[0]

def puzzle_1():
    with open("18.data", "r") as f:

        graph = nx.Graph()

        c_to_p = dict()
        p_to_c = dict()
        pos = (0,0)
        # Dict for each door, and which nodes can then be directly connected if the door is removed!
        door_connections = dict()

        # Build huge graph with every position (x,y) having its own edge to their neighbors.
        for y, line in enumerate(f.read().splitlines()):
            if not line.startswith("//") and not line.strip() == "":
                for x, c in enumerate(line):
                    # add edge for empty or key spaces.
                    if c in ".@" or c.isalpha():
                        add_surrounding_edge(graph, (x,y))
                    if c.isalpha():
                        c_to_p[c] = (x,y)
                        p_to_c[(x,y)] = c
                    if c == "@":
                        pos = (x,y)
                        p_to_c[(x,y)] = c
                        c_to_p[c] = (x,y)

        def keys_on_the_way(path):
            for p in path[1:]:
                if p in p_to_c and p_to_c[p] == p_to_c[p].upper():
                    yield p_to_c[p].lower()

        node_dist = dict()
        node_keys = dict()

        for s in c_to_p.keys():
            node_dist[s] = dict()
            node_keys[s] = dict()
            for s2 in c_to_p.keys():
                node_dist[s][s2] = nx.shortest_path_length(graph, c_to_p[s], c_to_p[s2])
                node_keys[s][s2] = set(keys_on_the_way(nx.shortest_path(graph, c_to_p[s], c_to_p[s2])))

        # solution for puzzle 1:
        print(path_length_puzzle_1(node_dist, node_keys, c_to_p, p_to_c))


def path_length_puzzle_2(node_dist, node_keys, c_to_p, p_to_c, starting_positions):

    # set with all keys
    all_keys = {k for k in c_to_p.keys() if k.lower() == k and k not in ["1", "2", "3", "4"]}

    # (4xpaths, 4xscores, 4xnodes, found_keys)
    queue = [([[],[],[],[]], [0,0,0,0], ["1", "2", "3", "4"], set())]
    solutions = []

    current_best_score = 10000000000000000

    path_cache = dict()
    # if we have been at a specific situation with the same collected keys at a node, we can discard
    # the new path, if the score is higher than one we had before!
    situation_cache = dict()

    def find_paths_2(node, found_keys):
        remaining_keys = all_keys - found_keys
        for k in remaining_keys:
            # Do I have enough keys, to go to this one?
            if node_keys[node][k] != None and len(node_keys[node][k] - found_keys - {"1", "2", "3", "4"}) == 0:
                yield k

    while len(queue) > 0:

        #print(queue)
        new_queue = []
        for q in queue:

            should_continue = True

            score = sum(q[1])
            found_keys = q[3].union(set(q[2]))

            node_hash_2 = (tuple(q[2]), tuple(found_keys))
            if node_hash_2 in situation_cache:
                if situation_cache[node_hash_2] <= score:
                    continue
            situation_cache[node_hash_2] = score

            for i in range(4):
                path = q[0][i]

                node = q[2][i]
                #found_keys = q[3].union({node})




                #print("  keys 1: {}".format(found_keys))
                #if node in "1234":
                found_keys = found_keys - {"1", "2", "3", "4"}

                #print("  keys 2: {}".format(found_keys))

                if len(found_keys) == len(all_keys):
                    #solutions.append((path+[node], sum(q[1])))

                    paths = q[0][:]
                    paths[i] += [node]

                    solutions.append((paths, score))
                    #print(sum(q[1]), found_keys)


                    current_best_score = min(current_best_score, score)
                    should_continue = False
                    break

                # early exit, already too slow...
                if score >= current_best_score:
                    should_continue = False
                    break

                node_hash = (node, tuple(found_keys))

                if node_hash in path_cache:
                    all_paths = path_cache[node_hash]
                else:
                    all_paths = list(find_paths_2(node, found_keys))
                    #print("  {}".format(all_paths))

                if node_hash not in path_cache:
                    path_cache[node_hash] = all_paths

                for p in all_paths:
                    #new_queue.append((path+[node], score+node_dist[node][p], p, found_keys))

                    paths = q[0][:]
                    paths[i] += [node]

                    scores = q[1][:]
                    scores[i] += node_dist[node][p]

                    nodes = q[2][:]
                    nodes[i] = p

                    #print("  keys: {}".format(found_keys))

                    new_queue.append((paths, scores, nodes, found_keys))

                    #print("  {}".format(p))
            if not should_continue:
                continue

        queue = new_queue

    #print(solutions)
    return sorted(solutions, key=lambda x: x[1])[0][1]

def puzzle_2():
    with open("18.data", "r") as f:

        graph = nx.Graph()

        c_to_p = dict()
        p_to_c = dict()
        starting_positions = []

        # Build huge graph with every position (x,y) having its own edge to their neighbors.
        for y, line in enumerate(f.read().splitlines()):
            if not line.startswith("//") and not line.strip() == "":
                for x, c in enumerate(line):
                    # add edge for empty or key spaces.
                    if c in ".1234" or c.isalpha():
                        add_surrounding_edge(graph, (x,y))
                    if c.isalpha() or c in "1234":
                        c_to_p[c] = (x,y)
                        p_to_c[(x,y)] = c
                    if c in "1234":
                        starting_positions.append((x,y))

        def keys_on_the_way(path):
            for p in path[1:]:
                if p in p_to_c and p_to_c[p] == p_to_c[p].upper():
                    yield p_to_c[p].lower()

        node_dist = dict()
        node_keys = dict()

        for s in c_to_p.keys():
            node_dist[s] = dict()
            node_keys[s] = dict()
            for s2 in c_to_p.keys():

                if nx.has_path(graph, c_to_p[s], c_to_p[s2]):
                    node_dist[s][s2] = nx.shortest_path_length(graph, c_to_p[s], c_to_p[s2])
                    node_keys[s][s2] = set(keys_on_the_way(nx.shortest_path(graph, c_to_p[s], c_to_p[s2])))
                else:
                    node_dist[s][s2] = -1
                    node_keys[s][s2] = None

        print("positions: {}".format(starting_positions))

        # solution for puzzle 2:
        print(path_length_puzzle_2(node_dist, node_keys, c_to_p, p_to_c, starting_positions))


def main():

    #puzzle_1()
    puzzle_2()



if __name__ == "__main__":
    main()

# solution for 18.01: 2946
# solution for 18.02: 1222
