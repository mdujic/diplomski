import csv
import pytest

from rpq_evaluation.graph_database.graph import Graph


def initialize_facebook_graph() -> Graph:
    input_path = "rpq_evaluation/tests/facebook.csv"
    edges = set()
    graph = Graph()
    with open(input_path, "r") as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            # string is in form "N##->N## :A"
            source, target = list(
                map(int, row[0].split(" ")[0].replace('N', '').split('->'))
            )
            edges.add((source, target))

    # sort edges first by source, then by target
    edges = sorted(edges, key=lambda x: (x[0], x[1]))

    for edge in edges:
        graph.add_edge(*edge, 'a')

    graph.end_inserts()

    return graph


@pytest.mark.parametrize(
    "regex, expected",
    [
        ('a*', 4039),
    ]
)
def test_facebook_any_walk(regex, expected):
    graph = initialize_facebook_graph()
    paths, _ = graph.any_walk(0, regex)
    assert len(paths) == expected


@pytest.mark.parametrize(
    "regex, expected",
    [
        ('a*', 18998),
    ]
)
def test_facebook_all_shortest_walk(regex, expected):
    graph = initialize_facebook_graph()
    groups, _ = graph.all_shortest_walk(0, regex, limit = 100000)
    assert sum(len(group) for group in groups) == expected


@pytest.mark.parametrize(
    "restrictor, selector, expected",
    [
        ("trail", "all_shortest", 10000), #timeout
        ("simple", "all_shortest", 10000), #timeout
        ("acyclic", "all_shortest", 10000), #timeout
        ("simple", "", 10000),  #timeout
        ("acyclic", "", 10000), #timeout
        ("trail", "", 10000),   #timeout
        ("simple", "any", 1102),
        ("acyclic", "any", 1102),
        ("trail", "any", 1102),
        ("simple", "any_shortest", 3261),
        ("acyclic", "any_shortest", 3261),
        ("trail", "any_shortest", 3261),
    ]
)
def test_facebook_restricted(restrictor, selector, expected):
    graph = initialize_facebook_graph()
    solutions, timeout = graph.restricted_paths(
        0, "a*", restrictor, selector, limit = 10000, timeout = 5
    )
    assert len(solutions) == expected
