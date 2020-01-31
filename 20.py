import networkx as nx
from networkx.algorithms.shortest_paths.weighted import single_source_dijkstra
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

def get_portal_name(field, p):
    if field[p[1]+1][p[0]].isalpha():
        return "{}{}".format(field[p[1]+1][p[0]], field[p[1]+2][p[0]])
    if field[p[1]-1][p[0]].isalpha():
        return "{}{}".format(field[p[1]-2][p[0]], field[p[1]-1][p[0]])
    if field[p[1]][p[0]+1].isalpha():
        return "{}{}".format(field[p[1]][p[0]+1], field[p[1]][p[0]+2])
    if field[p[1]][p[0]-1].isalpha():
        return "{}{}".format(field[p[1]][p[0]-2], field[p[1]][p[0]-1])

def is_portal(field, p):
    return  field[p[1]+1][p[0]].isalpha() or field[p[1]-1][p[0]].isalpha() or field[p[1]][p[0]+1].isalpha() or field[p[1]][p[0]-1].isalpha()


def puzzle_1(field, portals, portal_map, graph):
    final_graph = nx.Graph()

    for p1 in portals:
        for p2 in portals:
            if p1 != p2:
                for p1_pos in portal_map[p1]:
                    for p2_pos in portal_map[p2]:

                        # Combine the two portals by using the same name and create a new graph that removes the "portal" and
                        # directly connects all nodes to each other. Just a normal graph now, that we can throw Dijkstra on.
                        if nx.has_path(graph, p1_pos, p2_pos) and not final_graph.has_edge(p1, p2):
                            final_graph.add_edge(p1, p2, weight=nx.shortest_path_length(graph, p1_pos, p2_pos))

    step_count, steps = single_source_dijkstra(final_graph, "AA", "ZZ")

    return step_count + len(steps)-2

def is_outer(field, p):
    if field[p[1]-1][p[0]].isalpha() and field[p[1]+1][p[0]] == ".":
        # upper part of the field is outer, otherwise inner (from below)
        return p[1] <= len(field)/2
    if field[p[1]+1][p[0]].isalpha() and field[p[1]-1][p[0]] == ".":
        return p[1] >= len(field)/2

    if field[p[1]][p[0]+1].isalpha() and field[p[1]][p[0]-1] == ".":
        return p[0] >= len(field[p[1]])/2
    if field[p[1]][p[0]-1].isalpha() and field[p[1]][p[0]+1] == ".":
        return p[0] <= len(field[p[1]])/2
    return None


def puzzle_2(field, portals, portal_map, graph):
    final_graph = nx.Graph()

    # If using all levels we can at maximum go down half of all portals and half up again...?
    # Could be wrong, then remove the //2, but seems to work for this problem.
    for level in range(len(portals)//2):
        for p1 in portals:
            for p2 in portals:
                if p1 != p2:
                    # Only the first level has AA and ZZ.
                    if level > 0 and (p1 in ["AA", "ZZ"] or p2 in ["AA", "ZZ"]):
                        continue

                    for p1_pos in portal_map[p1]:

                        # The name is now unique for portals depending on level and inner/outer status!
                        outer_p1 = is_outer(field, p1_pos)
                        new_name_p1 = p1 + ("o" if outer_p1 else "i") + ("-" * level)

                        for p2_pos in portal_map[p2]:

                            # The name is now unique for portals depending on level and inner/outer status!
                            outer_p2 = is_outer(field, p2_pos)
                            new_name_p2 = p2 + ("o" if outer_p2 else "i") + ("-" * level)

                            if nx.has_path(graph, p1_pos, p2_pos):
                                final_graph.add_edge(new_name_p1, new_name_p2, weight=nx.shortest_path_length(graph, p1_pos, p2_pos))

                            # Portals going up
                            if outer_p1 and level > 0:
                                final_graph.add_edge(new_name_p1, new_name_p1.replace("o", "i")[:-1], weight=1)

                            # Portals going down
                            if not outer_p1 and p1 not in ["AA", "ZZ"]:
                                final_graph.add_edge(new_name_p1, new_name_p1.replace("i", "o") + "-", weight=1)


    # Go from the outer ports (though there are no inner) from AA to ZZ.
    step_count, steps = single_source_dijkstra(final_graph, "AAo", "ZZo")
    return step_count

def main():

    with open("20.data", "r") as f:

        graph = nx.Graph()

        field = []

        # BC --> (x,y) as a graph node.
        portal_map = defaultdict(list)
        portals = []

        # Read graph into array first
        for y, line in enumerate(f.read().splitlines()):
            if not line.startswith("//") and not line.strip() == "":
                field.append(line)

        # Build huge graph with every position (x,y) having its own edge to their neighbors.
        for y, line in enumerate(field):
            for x, c in enumerate(line):
                # add edge for empty or key spaces.
                if c == ".":
                    add_surrounding_edge(graph, (x,y))

                    if is_portal(field, (x,y)):
                        name = get_portal_name(field, (x,y))
                        portals.append(name)
                        portal_map[name].append((x,y))

        print("Puzzle 1: {}".format(puzzle_1(field, portals, portal_map, graph)))
        print("Puzzle 2: {}".format(puzzle_2(field, portals, portal_map, graph)))

if __name__ == "__main__":
    main()

# solution for 20.01: 654
# solution for 20.02: 7360
