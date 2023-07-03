import pytest

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

def initialize_with_b_at_the_end(n) -> Graph:
    assert not n % 3

    graph = Graph()

    for i in range(0, n, 3):
        graph.add_edge(i, i+1, 'a')
        graph.add_edge(i, i+2, 'a')
        graph.add_edge(i+1, i+3, 'a' if i + 3 < n else 'b')
        graph.add_edge(i+2, i+3, 'a' if i + 3 < n else 'b')

    graph.end_inserts()

    return graph


@pytest.mark.parametrize(
    "max_n, step, shortest, limit, timeout",
    [
        (1500, 102, True, 10**5, 60),
        (1500, 102, False, 10**5, 60),
        (1500, 102, True, 1, 60),
        (1500, 102, False, 1, 60),
    ]
)
def test_any_walk(max_n, step, shortest, limit, timeout):
    print("\n" + "+------------------------------------+")
    print(f"max_n: {max_n}, shortest: {shortest}, limit: {limit}, timeout: {timeout}")
    file_name = f"rpq_evaluation/tests/test_diamond_results/any_shortest_walk_{max_n}_{shortest}_{limit}_{timeout}.csv"
    # open file for writing and append results
    f = open(file_name, "a")
    f.write("n,path,time\n")
    print("+------------------------------------+")
    print("n,path,time")
    for n in range(0, max_n, step):
        graph = initialize_graph(n)

        solutions, time_ = graph.any_walk(
            v=0,
            regex='a*',
            shortest=shortest,
            limit=limit,
            timeout=timeout
        )
        print(f"{n+1},{len(solutions)},{time_}")
        f.write(f"{n+1},{len(solutions)},{time_}\n")
        assert not n or len(solutions) == min(n + 1, limit + 1)
    f.write("\n")
    f.close()
    print("\n" + "*------------------------------------*")


@pytest.mark.parametrize(
    "max_n, step, shortest, limit, timeout",
    [
        (1500, 102, True, 10, 60),
        (1500, 102, False, 10, 60),
    ]
)
def test_any_walk_one_solution(max_n, step, shortest, limit, timeout):
    print("\n" + "+------------------------------------+")
    print(f"max_n: {max_n}, shortest: {shortest}, limit: {limit}, timeout: {timeout}")
    file_name = f"rpq_evaluation/tests/test_diamond_results/any_shortest_walk_one_solution_{max_n}_{shortest}_{limit}_{timeout}.csv"
    # open file for writing and append results
    f = open(file_name, "a")
    f.write("n,path,time\n")
    print("+------------------------------------+")
    print("n,path,time")
    for n in range(0, max_n, step):
        graph = initialize_with_b_at_the_end(n)

        solutions, time_ = graph.any_walk(
            v=0,
            regex='a*b',
            shortest=shortest,
            limit=limit,
            timeout=timeout
        )
        print(f"{n+1},{len(solutions)},{time_}")
        f.write(f"{n+1},{len(solutions)},{time_}\n")
        assert not n or len(solutions) == 1
    f.write("\n")
    f.close()
    print("\n" + "*------------------------------------*")



@pytest.mark.parametrize(
    "max_n, step, limit, timeout",
    [
        (46, 3, 10**5, 60),
        (46, 3, 1, 60),
    ]
)
def test_all_shortest_walk(max_n, step, limit, timeout):
    print("\n" + "+------------------------------------+")
    print(f"max_n: {max_n}, limit: {limit}, timeout: {timeout}")
    print("+------------------------------------+")
    file_name = f"rpq_evaluation/tests/test_diamond_results/all_shortest_walk_{max_n}_{limit}_{timeout}.csv"
    # open file for writing and append results
    f = open(file_name, "a")
    f.write("n,total_paths,time\n")
    for n in range(0, max_n, step):
        graph = initialize_graph(n)

        total_paths = 0
        groups, time_ = graph.all_shortest_walk(
            0, 'a*', limit=limit, timeout=timeout
        )
        for group in groups:
            total_paths += len(group)
        print(f"{n+1},{total_paths},{time_}")
        f.write(f"{n+1},{total_paths},{time_}\n")
        assert total_paths == min(2**((n + 8)//3) - 3, limit)
    f.write("\n")
    f.close()
    print("\n" + "*------------------------------------*")


@pytest.mark.parametrize(
    "restrictor, selector, max_n, step, limit, timeout",
    [
        ("trail", "all_shortest", 46, 3, 10**5, 60),
        ("simple", "all_shortest", 46, 3, 10**5, 60),
        ("acyclic", "all_shortest", 46, 3, 10**5, 60),
        ("simple", "", 46, 3, 10**5, 60),
        ("acyclic", "", 46, 3, 10**5, 60),
        ("trail", "", 46, 3, 10**5, 60),
        ("simple", "any", 46, 3, 10**5, 60),
        ("acyclic", "any", 46, 3, 10**5, 60),
        ("trail", "any", 46, 3, 10**5, 60),
        ("simple", "any_shortest", 46, 3, 10**5, 60),
        ("acyclic", "any_shortest", 46, 3, 10**5, 60),
        ("trail", "any_shortest", 46, 3, 10**5, 60),
        ("trail", "all_shortest", 46, 3, 10, 60),
        ("simple", "all_shortest", 46, 3, 10, 60),
        ("acyclic", "all_shortest", 46, 3, 10, 60),
        ("simple", "", 46, 3, 10, 60),
        ("acyclic", "", 46, 3, 10, 60),
        ("trail", "", 46, 3, 10, 60),
        ("simple", "any", 46, 3, 10, 60),
        ("acyclic", "any", 46, 3, 10, 60),
        ("trail", "any", 46, 3, 10, 60),
        ("simple", "any_shortest", 46, 3, 10, 60),
        ("acyclic", "any_shortest", 46, 3, 10, 60),
        ("trail", "any_shortest", 46, 3, 10, 60),

    ]
)
def test_restricted(restrictor, selector, max_n, step, limit, timeout):
    file_name = f"rpq_evaluation/tests/test_diamond_results/restricted_{restrictor}_{selector}_{max_n}_{limit}_{timeout}.csv"
    f = open(file_name, "a")

    for n in range(0, max_n, step):
        graph = initialize_graph(n)
        # open file for writing and append results
        f.write("n,total_paths,time\n")
        solutions, time_ = graph.restricted_paths(
            v=0,
            regex='a*',
            restrictor=restrictor,
            selector=selector,
            limit=limit,
            timeout=timeout
        )
        f.write(f"{n+1},{len(solutions)},{time_}\n")
        print(f"{n+1},{len(solutions)},{time_}")
        if "any" in selector:
            assert not n or len(solutions) == min(n + 1, limit)
        else:
            assert not n or len(solutions) == min(2**((n + 8)//3) - 3, limit)


@pytest.mark.parametrize(
    "restrictor, selector, max_n, step, limit, timeout",
    [
        ("simple", "any", 46, 3, 10**5, 60),
        ("acyclic", "any", 46, 3, 10**5, 60),
        ("trail", "any", 46, 3, 10**5, 60),
        ("simple", "any_shortest", 46, 3, 10**5, 60),
        ("acyclic", "any_shortest", 46, 3, 10**5, 60),
        ("trail", "any_shortest", 46, 3, 10**5, 60),
    ]
)
def test_restricted_one_solution(restrictor, selector, max_n, step, limit, timeout):
    file_name = f"rpq_evaluation/tests/test_diamond_results/restricted_one_solution_{restrictor}_{selector}_{max_n}_{limit}_{timeout}.csv"
    f = open(file_name, "a")

    for n in range(0, max_n, step):
        graph = initialize_with_b_at_the_end(n)
        # open file for writing and append results
        f.write("n,total_paths,time\n")
        solutions, time_ = graph.restricted_paths(
            v=0,
            regex='a*b',
            restrictor=restrictor,
            selector=selector,
            limit=limit,
            timeout=timeout
        )
        f.write(f"{n+1},{len(solutions)},{time_}\n")
        print(f"{n+1},{len(solutions)},{time_}")
        assert not n or len(solutions) == 1
