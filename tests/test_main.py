from graph_database.graph import Graph


def test_rpq_eval():
    graph = Graph()
    graph.add_edge(0, 1, 'a')
    graph.add_edge(0, 2, 'b')
    graph.add_edge(0, 5, 'a')
    graph.add_edge(1, 3, 'a')
    graph.add_edge(1, 4, 'b')
    graph.add_edge(2, 1, 'a')
    graph.add_edge(2, 4, 'b')
    graph.add_edge(3, 2, 'a')
    graph.add_edge(3, 4, 'b')

    graph.end_inserts()

    assert graph.rpq_eval(0, 'ab') == [[0, 1, 4]]


def test_all_shortest_rpq_eval():
    graph = Graph()
    graph.add_edge(0, 1, 'a')
    graph.add_edge(0, 2, 'b')
    graph.add_edge(0, 5, 'a')
    graph.add_edge(1, 3, 'a')
    graph.add_edge(1, 4, 'b')
    graph.add_edge(2, 1, 'a')
    graph.add_edge(2, 4, 'b')
    graph.add_edge(3, 2, 'a')
    graph.add_edge(3, 4, 'b')

    graph.end_inserts()

    assert graph.all_shortest_rpq_eval(0, 'aa+ab+ba+bb') == [[0, 2, 4], [0, 2, 1], [0, 1, 4], [0, 1, 3]]