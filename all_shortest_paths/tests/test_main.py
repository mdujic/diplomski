from all_shortest_paths.graph_database.graph import Graph

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


def test_any_walk():
    assert graph.any_walk(0, 'a*') == [
        [0],
        [0, (0, 'a', 1), 1],
        [0, (0, 'a', 5), 5],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3, (3, 'a', 2), 2]
    ]

def test_any_shortest_walk():
    assert graph.any_walk(0, '(a+b)*', True) == [
        [0],
        [0, (0, 'a', 1), 1],
        [0, (0, 'a', 5), 5],
        [0, (0, 'b', 2), 2],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3],
        [0, (0, 'a', 1), 1, (1, 'b', 4), 4]
    ]

def test_all_shortest_walk():
    assert graph.all_shortest_walk(0, 'a*') == [
        [
            [0]
        ],
        [
            [0, (0, 'a', 1), 1]
        ],
        [
            [0, (0, 'a', 5), 5]
        ],
        [
            [0, (0, 'a', 1), 1, (1, 'a', 3), 3]
        ],
        [
            [0, (0, 'a', 1), 1, (1, 'a', 3), 3, (3, 'a', 2), 2]
        ]
    ]


def test_all_shortest_huge():

    a = 800
    graph = Graph()
    for i in range(a):
        graph.add_edge(i, i+1, 'a')
        graph.add_edge(i, i+1, 'b')

    graph.end_inserts()

    count = len(graph.all_shortest_rpq_eval(0, '(a+b)*'))
    assert count == a + 1
