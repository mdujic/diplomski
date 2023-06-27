from rpq_evaluation.graph_database.graph import Graph

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
    assert graph.any_walk(0, 'a*')[0] == [
        [0],
        [0, (0, 'a', 1), 1],
        [0, (0, 'a', 5), 5],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3, (3, 'a', 2), 2]
    ]

def test_any_shortest_walk():
    assert graph.any_walk(0, '(a+b)*', True)[0] == [
        [0],
        [0, (0, 'a', 1), 1],
        [0, (0, 'a', 5), 5],
        [0, (0, 'b', 2), 2],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3],
        [0, (0, 'a', 1), 1, (1, 'b', 4), 4]
    ]

def test_all_shortest_walk():
    assert graph.all_shortest_walk(0, 'a*')[0] == [
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

def test_all_shortest_trail():
    assert graph.restricted_paths(0, 'a*', "trail", "all_shortest")[0] == [
        [0],
        [0, (0, 'a', 1), 1],
        [0, (0, 'a', 5), 5],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3, (3, 'a', 2), 2]
    ]

def test_all_shortest_simple():
    assert graph.restricted_paths(0, 'a*', "simple", "all_shortest")[0] == [
        [0],
        [0, (0, 'a', 1), 1],
        [0, (0, 'a', 5), 5],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3, (3, 'a', 2), 2]
    ]

def test_all_shortest_acyclic():
    assert graph.restricted_paths(0, 'a*', "acyclic", "all_shortest")[0] == [
        [0],
        [0, (0, 'a', 1), 1],
        [0, (0, 'a', 5), 5],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3, (3, 'a', 2), 2]
    ]

def test_simple():
    assert graph.restricted_paths(0, 'a*', "simple", "")[0] == [
        [0],
        [0, (0, 'a', 1), 1],
        [0, (0, 'a', 5), 5],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3, (3, 'a', 2), 2]
    ]

def test_acyclic():
    assert graph.restricted_paths(0, 'a*', "acyclic", "")[0] ==  [
        [0],
        [0, (0, 'a', 1), 1],
        [0, (0, 'a', 5), 5],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3, (3, 'a', 2), 2]
    ]

def test_trail():
    assert graph.restricted_paths(0, 'a*', "trail", "")[0] == [
        [0],
        [0, (0, 'a', 1), 1],
        [0, (0, 'a', 5), 5],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3, (3, 'a', 2), 2],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3, (3, 'a', 2), 2, (2, 'a', 1), 1]
    ]


def test_any_simple():
    assert graph.restricted_paths(0, 'a*', "simple", "any")[0] ==  [
        [0],
        [0, (0, 'a', 1), 1],
        [0, (0, 'a', 5), 5],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3, (3, 'a', 2), 2]
    ]

def test_any_acyclic():
    assert graph.restricted_paths(0, 'a*', "acyclic", "any")[0] ==  [
        [0],
        [0, (0, 'a', 1), 1],
        [0, (0, 'a', 5), 5],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3, (3, 'a', 2), 2]
    ]

def test_any_trail():
    assert graph.restricted_paths(0, 'a*', "trail", "any")[0] ==  [
        [0],
        [0, (0, 'a', 1), 1],
        [0, (0, 'a', 5), 5],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3, (3, 'a', 2), 2]
    ]

def test_any_shortest_simple():
    assert graph.restricted_paths(0, 'a*', "simple", "any_shortest")[0] ==  [
        [0],
        [0, (0, 'a', 1), 1],
        [0, (0, 'a', 5), 5],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3, (3, 'a', 2), 2]
    ]

def test_any_shortest_acyclic():
    assert graph.restricted_paths(0, 'a*', "acyclic", "any_shortest")[0] ==  [
        [0],
        [0, (0, 'a', 1), 1],
        [0, (0, 'a', 5), 5],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3, (3, 'a', 2), 2]
    ]

def test_any_shortest_trail():
    assert graph.restricted_paths(0, 'a*', "trail", "any_shortest")[0] ==  [
        [0],
        [0, (0, 'a', 1), 1],
        [0, (0, 'a', 5), 5],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3, (3, 'a', 2), 2]
    ]
