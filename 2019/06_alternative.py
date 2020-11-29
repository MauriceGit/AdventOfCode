import networkx as nx


if __name__ == "__main__":

    with open("06.data", "r") as f:

        graph = nx.Graph()

        for o in f.read().splitlines():
            graph.add_edge(*o.split(")")[:2])

        count = 0
        for n in graph.nodes:
            count += nx.shortest_path_length(graph, n, "COM")

        print(count)
        print(nx.shortest_path_length(graph, "YOU", "SAN") -2)


# solution for 06.01: 292387
# solution for 06.02: 433
