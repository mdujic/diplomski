from rpq_evaluation.graph_database.graph import Graph


def initialize_graph(n) -> Graph:
    graph = Graph()

    for i in range(0, n, 3):
        graph.add_edge(i, i+1, 'a')
        graph.add_edge(i, i+2, 'a')
        graph.add_edge(i+1, i+3, 'a')
        graph.add_edge(i+2, i+3, 'a')

    graph.end_inserts()

    return graph


def test_all_shortest_walk():
    for n in range(100):
        graph = initialize_graph(n)

        total_paths = 0
        for groups in graph.all_shortest_walk(0, 'a*')[0]:
            total_paths += len(groups)
        print(f"n: {n}, total_paths: {total_paths}")

        if n <= 33:
            assert total_paths == 2**((n + 8)//3) - 3
        else:
            assert total_paths == 10000


def test_all_shortest_walk_timeout():
    graph = initialize_graph(100)

    total_paths = 0
    _, time_ = graph.all_shortest_walk(0, 'a*', limit = 10000, timeout = 0.1)
    assert time_ < 0.2

