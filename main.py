from graph import Graph

def main():
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

    graph.all_shortest_rpq_eval(0, '(a+b)(a+b)')


if __name__ == '__main__':
    main()