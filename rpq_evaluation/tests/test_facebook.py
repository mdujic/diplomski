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
    "v, regex, shortest, limit, timeout",
    [
        (0, 'a*', True, 10**5, 60),
        (0, 'a*', False, 10**5, 60),
        (0, 'a*', True, 10, 60),
        (0, 'a*', False, 10, 60),
        (1123, 'a*', True, 10**5, 60),
        (1123, 'a*', False, 10**5, 60),
        (1123, 'a*', True, 10, 60),
        (1123, 'a*', False, 10, 60),
        (3754, 'a*', True, 10**5, 60),
        (3754, 'a*', False, 10**5, 60),
        (3754, 'a*', True, 10, 60),
        (3754, 'a*', False, 10, 60),
        (1543, 'a*', True, 10**5, 60),
        (1543, 'a*', False, 10**5, 60),
        (1543, 'a*', True, 10, 60),
        (1542, 'a*', False, 10, 60),
    ]
)
def test_any_walk(v, regex, shortest, limit, timeout):
    graph = initialize_facebook_graph()
    print("\n" + "+------------------------------------+")
    print(f"v: {v}, shortest: {shortest}, limit: {limit}, timeout: {timeout}")
    print("+------------------------------------+")
    file_name = f"rpq_evaluation/tests/test_facebook_results/any_shortest_walk_{v}_{shortest}_{limit}_{timeout}.csv"
    # open file for writing and append results
    f = open(file_name, "a")
    f.write("path,time\n")
    paths, time_ = graph.any_walk(
        v=v,
        regex=regex,
        shortest=shortest,
        limit=limit,
        timeout=timeout
    )
    print(f"{len(paths)},{time_}")
    f.write(f"{len(paths)},{time_}\n")
    f.write("\n")
    f.close()

    assert len(paths) <= limit and time_ <= timeout
    print("*------------------------------------*")


@pytest.mark.parametrize(
    "v, regex, limit, timeout",
    [
        (0, 'a*', 10**5, 60),
        (0, 'a*', 10, 60),
        (1123, 'a*', 10**5, 60),
        (1123, 'a*', 10, 60),
        (3754, 'a*', 10**5, 60),
        (3754, 'a*', 10, 60),
        (1543, 'a*', 10**5, 60),
        (1543, 'a*', 10, 60),
    ]
)
def test_all_shortest_walk(v, regex, limit, timeout):
    graph = initialize_facebook_graph()
    print("\n" + "+------------------------------------+")
    print(f"v: {v}, limit: {limit}, timeout: {timeout}")
    print("+------------------------------------+")
    file_name = f"rpq_evaluation/tests/test_facebook_results/all_shortest_walk_{v}_{limit}_{timeout}.csv"
    # open file for writing and append results
    f = open(file_name, "a")
    f.write("path,time\n")
    groups, time_ = graph.all_shortest_walk(
        v=v,
        regex=regex,
        limit=limit,
        timeout=timeout
    )
    len_paths = sum(len(group) for group in groups)
    print(f"{len_paths},{time_}")
    f.write(f"{len_paths},{time_}\n")
    f.write("\n")
    f.close()
    assert len_paths <= limit and time_ <= timeout
    print("*------------------------------------*")

@pytest.mark.parametrize(
    "restrictor, selector, limit, timeout",
    [
        ("trail", "all_shortest", 10**5, 1),
        ("simple", "all_shortest", 10**5, 1),
        ("acyclic", "all_shortest", 10**5, 1),
        ("simple", "", 10**5, 1),
        ("acyclic", "", 10**5, 1),
        ("trail", "", 10**5, 1),
        ("simple", "any", 10**5, 1),
        ("acyclic", "any", 10**5, 1),
        ("trail", "any", 10**5, 1),
        ("simple", "any_shortest", 10**5, 1),
        ("acyclic", "any_shortest", 10**5, 1),
        ("trail", "any_shortest", 10**5, 1),
        ("trail", "all_shortest", 10, 60),
        ("simple", "all_shortest", 10, 60),
        ("acyclic", "all_shortest", 10, 60),
        ("simple", "", 10, 60),
        ("acyclic", "", 10, 60),
        ("trail", "", 10, 60),
        ("simple", "any", 10, 60),
        ("acyclic", "any", 10, 60),
        ("trail", "any", 10, 60),
        ("simple", "any_shortest", 10, 60),
        ("acyclic", "any_shortest", 10, 60),
        ("trail", "any_shortest", 10, 60),
    ]
)
def test_restricted(restrictor, selector, limit, timeout,):
    graph = initialize_facebook_graph()
    print("\n" + "+------------------------------------+")
    print(f"restrictor: {restrictor}, selector: {selector}, limit: {limit}, timeout: {timeout}")
    print("+------------------------------------+")
    file_name = f"rpq_evaluation/tests/test_facebook_results/restricted_{restrictor}_{selector}_{limit}_{timeout}.csv"
    # open file for writing and append results
    f = open(file_name, "a")
    f.write("path,time\n")

    solutions, time_ = graph.restricted_paths(
        v=0,
        regex="a*",
        restrictor=restrictor,
        selector=selector,
        limit=limit,
        timeout=timeout
    )
    print(f"{len(solutions)},{time_}")
    f.write(f"{len(solutions)},{time_}\n")
    f.write("\n")
    f.close()
    assert len(solutions) <= limit and time_ <= timeout + 0.01
    print("*------------------------------------*")
