import pytest

from rpq_evaluation.graph_database.graph import Graph

def initialize_simple_graph() -> Graph:
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

    return graph

@pytest.mark.parametrize(
    "regex, expected, is_shortest",
    [
        ('a*', [
            [0], [0, (0, 'a', 1), 1],
            [0, (0, 'a', 5), 5],
            [0, (0, 'a', 1), 1, (1, 'a', 3), 3],
            [0, (0, 'a', 1), 1, (1, 'a', 3), 3, (3, 'a', 2), 2]],
            False
        ),
        ('(a+b)*', [
            [0],
            [0, (0, 'a', 1), 1],
            [0, (0, 'a', 5), 5],
            [0, (0, 'b', 2), 2],
            [0, (0, 'a', 1), 1, (1, 'a', 3), 3],
            [0, (0, 'a', 1), 1, (1, 'b', 4), 4]],
            True
        ),
    ]
)
def test_any_walk(regex, expected, is_shortest):
    graph = initialize_simple_graph()
    assert graph.any_walk(0, regex, is_shortest)[0] == expected


def test_all_shortest_walk():
    graph = initialize_simple_graph()
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


@pytest.mark.parametrize(
    "restrictor, selector",
    [
        ("trail", "all_shortest"),
        ("simple", "all_shortest"),
        ("acyclic", "all_shortest"),
        ("simple", ""),
        ("acyclic", ""),
        ("trail", ""),
        ("simple", "any"),
        ("acyclic", "any"),
        ("trail", "any"),
        ("simple", "any_shortest"),
        ("acyclic", "any_shortest"),
        ("trail", "any_shortest"),
    ]
)
def test_all_shortest_trail(restrictor, selector):
    graph = initialize_simple_graph()
    assert graph.restricted_paths(0, 'a*', restrictor, selector)[0] == ([
        [0],
        [0, (0, 'a', 1), 1],
        [0, (0, 'a', 5), 5],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3],
        [0, (0, 'a', 1), 1, (1, 'a', 3), 3, (3, 'a', 2), 2]
    ] if not (restrictor == "trail" and not selector)
    else
     [
         [0],
         [0, (0, 'a', 1), 1],
         [0, (0, 'a', 5), 5],
         [0, (0, 'a', 1), 1, (1, 'a', 3), 3],
         [0, (0, 'a', 1), 1, (1, 'a', 3), 3, (3, 'a', 2), 2],
         [0, (0, 'a', 1), 1, (1, 'a', 3), 3, (3, 'a', 2), 2, (2, 'a', 1), 1]
     ])
