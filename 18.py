import networkx as nx
from utility import add_p
import matplotlib.pyplot as plt
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

def step_count(graph, special, p0, p1):
    n0 = p0
    n1 = p1
    if p0 in special:
        n0 = special[p0]
    if p1 in special:
        n1 = special[p1]
    try:
        return nx.shortest_path_length(graph, n0, n1)
    except:
        return 0

def remove_door(graph, pos):
    add_surrounding_edge(graph, pos)

def path_length(graph, special, pos):

    reachable = list(filter(lambda x: x[1] != 0, [(p, step_count(graph, special, pos, p)) for p in special]))

    if len(reachable) == 0:
        return [], 0

    min_dist = 1000000000000000
    min_path = []
    for r in reachable:

        current_special = special.copy()
        current_graph = graph.copy()

        target = r[0]
        target_p = current_special[r[0]]
        # Remove road blocks
        if r[0].upper() in current_special:
            remove_door(current_graph, current_special[r[0].upper()])
            del current_special[r[0].upper()]
        del current_special[r[0].lower()]

        path, score = path_length(current_graph, current_special, target_p)
        if score+r[1] < min_dist:
            min_dist = score+r[1]
            min_path = [target] + path

    return min_path, min_dist




def path_length_dfs(graph, p_to_c, last_node, node, blocked_nodes, remaining_keys, already_visited):

    if len(remaining_keys - {p_to_c[node]}) == 0:
        return [], 0

    if (last_node, node) in already_visited:
        return [], 100000000000000000

    is_door = graph.node[node]["is_door"]

    #print("calc length for node: {} with keys: {} ".format(node, remaining_keys))


    min_dist = 100000000000000000
    min_path = []

    for e in graph.edges(node, data=True):

        # Don't go back, if:
        #   we are at a door (because it is unlocked, it's just a transit )
        #   we are at a key that is already collected

        if not graph.node[e[1]]["is_door"] or not p_to_c[e[1]] in blocked_nodes:

            # we are at @
            if p_to_c[e[0]] == "@" and e[1] == last_node:
                continue

            # unlocked door
            if is_door and e[1] == last_node:
                continue

            # already collected key
            if not is_door and p_to_c[e[0]] != "@" and p_to_c[e[0]] not in remaining_keys and e[1] == last_node:
                continue

            path, score = path_length_dfs(graph, p_to_c, e[0], e[1], blocked_nodes - {p_to_c[e[0]].upper()}, remaining_keys - {p_to_c[e[0]]}, already_visited.union({(last_node, node)}))

            w = e[2]["weight"]
            if score + w < min_dist:
                min_dist = score + w
                min_path = [e[0]] + path

    return min_path, min_dist

# Get list of neighbors that have not yet been visited!
# So no used key fields, no opened doors, no @.
def get_valid_neighbors(graph, p_to_c, node, blocked_nodes, remaining_keys, last_nodes=set()):


    #print("    last_nodes: {}".format(last_nodes))

    neighbor_nodes = []
    for e in graph.edges(node, data=True):


        #print("    try: {}".format(e))

        # (x,y)
        n_p = e[1]
        # 'c'
        n_c = p_to_c[n_p]

        # do not go back here!
        if n_p in last_nodes:
            #print("      been here")
            continue
        # valid node, if it is a key we've not yet picked up!
        if n_c in remaining_keys:
            #print("      Nice.")
            neighbor_nodes.append(e)
            continue
        # cannot go to blocked nodes yet
        if n_c in blocked_nodes:
            #print("      blocked")
            continue

        neighbor_nodes.extend(get_valid_neighbors(graph, p_to_c, n_p, blocked_nodes, remaining_keys, last_nodes.union({node})))

    return neighbor_nodes


# Get list of neighbors that have not yet been visited!
# So no used key fields, no opened doors, no @.
def get_valid_neighbors2(graph, p_to_c, node, blocked_nodes, remaining_keys, last_nodes=set(), weight=0):


    neighbor_nodes = []
    for e in graph.edges(node, data=True):

        # (x,y)
        n_p = e[1]
        # 'c'
        n_c = p_to_c[n_p]

        # do not go back here!
        if n_p in last_nodes:
            #print("      been here")
            continue
        # valid node, if it is a key we've not yet picked up!
        if n_c in remaining_keys:
            #print("      Nice.")
            #print("from {} found node {}".format(p_to_c[node], n_c))
            neighbor_nodes.append((e, weight+e[2]["weight"]))
            continue
        # cannot go to blocked nodes yet
        if n_c in blocked_nodes:
            #print("      blocked")
            continue

        neighbor_nodes.extend(get_valid_neighbors2(graph, p_to_c, n_p, blocked_nodes, remaining_keys, last_nodes.union({node}), weight+e[2]["weight"]))

    return neighbor_nodes


def path_length_bfs(graph, p_to_c, node, blocked_nodes, remaining_keys):

    # (path, score, node, blocked_nodes, remaining_keys)
    queue = [([], 0, node, blocked_nodes, remaining_keys)]
    solutions = []

    while len(queue) > 0:

        new_queue = []
        for q in queue:

            #print(q)

            path = q[0]
            score = q[1]
            node = q[2]
            blocked_nodes = q[3]
            remaining_keys = q[4]

            if len(remaining_keys - {p_to_c[node]}) == 0:
                solutions.append((path+[node], score))
                #print(solutions)
                continue

            new_blocked_nodes  = blocked_nodes-{p_to_c[node].upper()}
            new_remaining_keys = remaining_keys-{p_to_c[node]}

            neighbors = get_valid_neighbors2(graph, p_to_c, node, new_blocked_nodes, new_remaining_keys)
            #print("    ", neighbors)
            for e, w in neighbors:
                new_queue.append((path+[node], score+w, e[1], new_blocked_nodes, new_remaining_keys))


        queue = new_queue


    #print("Final solutions: {}".format(solutions))
    return sorted(solutions, key=lambda x: x[1])[0]


def main():



    with open("18.data", "r") as f:

        graph = nx.Graph()

        special = dict()
        special_nodes = dict()
        pos = (0,0)
        # Dict for each door, and which nodes can then be directly connected if the door is removed!
        door_connections = dict()

        # Build huge graph with every position (x,y) having its own edge to their neighbors.
        for y, line in enumerate(f.read().splitlines()):
            for x, c in enumerate(line):
                # add edge for empty or key spaces.
                if c in ".@" or c.isalpha():# and c == c.lower():
                    add_surrounding_edge(graph, (x,y))
                if c.isalpha():
                    special[c] = (x,y)
                    special_nodes[(x,y)] = c
                if c == "@":
                    pos = (x,y)
                    special_nodes[(x,y)] = c
                    special[c] = (x,y)

        new_graph = nx.Graph()
        # Clean up the huge graph to only include special nodes! No need for a labyrinth any more...!
        nodes = set(filter(lambda x: x in special_nodes, graph.nodes()))
        for n in nodes:
            for n2 in nodes:
                path = nx.shortest_path(graph, n, n2)
                # Not to itself and only to the next poi
                if len(path) > 1 and not new_graph.has_edge(path[0], path[-1]) and all([p not in special_nodes for p in path[1:-1]]):
                    new_graph.add_edge(path[0], path[-1], weight=len(path)-1)

        graph = None

        for s in special:
            new_graph.nodes[special[s]]["is_door"] = s == s.upper() and s != "@"


        blocked_nodes  = set(filter(lambda x: x == x.upper() and x != "@", special.keys()))
        remaining_keys = set(filter(lambda x: x == x.lower() and x != "@", special.keys()))

        #print("blocked nodes : {}".format(blocked_nodes))
        #print("remaining keys: {}".format(remaining_keys))

        #path, score = path_length_dfs(new_graph, special_nodes, special["@"], special["@"], blocked_nodes, remaining_keys, set())
        path, score = path_length_bfs(new_graph, special_nodes, special["@"], blocked_nodes, remaining_keys)

        print(score)
        print(list(map(lambda x: special_nodes[x], path)))



        #print(nx.shortest_path_length(new_graph, special["c"], special["d"], weight="weight"))
        #nx.draw(new_graph)
        #plt.show()

        #print(nx.all_pairs_shortest_path(new_graph))

        #print(step_count(graph, special, (21,1), "d"))
        #print(path_length(new_graph.copy(), special.copy(), pos))


if __name__ == "__main__":
    main()

# solution for 06.01:
# solution for 06.02:
