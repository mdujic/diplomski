import csv
import pytest

from rpq_evaluation.graph_database.graph import Graph

def initialize_wiki_graph(column: int = 3) -> (Graph, dict):
    '''
    Initialize the graph from the wikiRfA dataset.
    We use the second column as the source node, the third column as the target
    node, and the fourth or fifth column as the edge label.
    Strings are converted to integers and edge labels are converted to a, b, c.
    '''

    # column must be 3 or 4
    if column not in [3, 4]:
        raise Exception("Column must be 3 or 4")

    graph = Graph()

    input_path = "rpq_evaluation/tests/wikiRfA.csv"
    nodes = set()

    with open(input_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # skip header
        next(csv_reader)
        for row in csv_reader:
            nodes.add(row[1])
            nodes.add(row[2])

    node_map = {}

    other_rows_map = {
        '1': 'a',
        '-1': 'b',
        '0': 'c'
    }

    for i, node in enumerate(nodes):
        node_map[node] = i

    with open(input_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # copy header to output file
        header = next(csv_reader)
        edges = []
        for row in csv_reader:
            edge = (
                    node_map[row[1]],
                    node_map[row[2]],
                    other_rows_map[row[column]],
            )
            edges.append(edge)
        # sort edges by source node, then by target
        edges.sort(key=lambda x: (x[0], x[1]))

        # add edges to graph
        for edge in edges:
            graph.add_edge(*edge)

    graph.end_inserts()
    return graph, {v:k for k,v in node_map.items()}


@pytest.mark.parametrize(
    "regex, res, column",
    [
        ('a*', 2854, 3),
        ('b*', 2507, 3),
        ('c*', 1631, 3),
        ('(ab)*', 2491, 3),
        ('(a|c)*', 3062, 3),
        ('a*', 1876, 4),
        ('b*', 1747, 4),
        ('(a|b)*', 3461, 4),
    ]
)
def test_wiki_vote(regex, res, column):
    graph, node_map = initialize_wiki_graph(column)
    solutions, _ = graph.any_walk(0, regex)

    assert len(solutions) == res
