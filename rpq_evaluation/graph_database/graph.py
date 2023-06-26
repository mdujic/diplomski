from typing import List, Tuple
import uuid

from rpq_evaluation.graph_database.core.trie import Trie
from rpq_evaluation.regex_transform.automaton import Automaton


class Edge:
    def __init__(self, source: int, target: int, label: str):
        self.source = source
        self.target = target
        self.label = label
        self.id = uuid.uuid4()


class EdgeTrie:
    def __init__(self):
        self.trie_map = {}

    def insert(self, edge: Edge) -> None:
        if edge.label not in self.trie_map:
            self.trie_map[edge.label] = Trie()

        # Use source vertex as prefix and target vertex as data
        self.trie_map[edge.label].insert(edge.source, edge.target)

    def query(self, label: str, prefix: int) -> Tuple[List[int], List[int]]:
        if label not in self.trie_map:
            return []

        # Use prefix as query and return data as a list of target vertices
        return self.trie_map[label].query(prefix)

    def end_inserts(self):
        for trie in self.trie_map.values():
            trie.end_inserts()

BFS = 0
DFS = -1

class Graph:

    def __init__(self):
        self.edges = []
        self.edge_trie = EdgeTrie()

    def add_edge(self, source: int, target: int, label: str) -> None:
        edge = Edge(source, target, label)
        self.edges.append(edge)
        self.edge_trie.insert(edge)

    def query(self, label: str, prefix: int) -> List[int]:
        data = self.edge_trie.query(label, prefix)
        return data

    def end_inserts(self):
        self.edge_trie.end_inserts()

    def get_all_nodes(self) -> List[int]:
        nodes = set()
        for edge in self.edges:
            nodes.add(edge.source)
            nodes.add(edge.target)
        return list(nodes)


    def any_walk(self, v: int, regex: str, shortest: bool = False) -> List:
        solutions = []
        A = Automaton(regex)

        start_search_state = (v, A.start_state, None, None)
        open_list = [start_search_state]
        visited = set()
        visited.add((v, A.start_state))
        reached_final = set()
        if v in self.get_all_nodes() and A.start_state in A.final_states:
            reached_final.add(v)
            solutions.append([v])

        search_type_selector = BFS if shortest else DFS
        while open_list:
            # current = (node, state, edge, prev)
            current = open_list.pop(search_type_selector)
            n, q, edge, prev = current
            for n_, q_, edge_ in self.get_neighbors(n, q, A):
                if (n_, q_) not in visited:
                    new_search_state = (n_, q_, edge_, current)
                    visited.add((n_, q_))
                    open_list.append(new_search_state)
                    if q_ in A.final_states and n_ not in reached_final:
                        reached_final.add(n_)
                        path = self.get_path(current) + [edge_, n_]
                        solutions.append(path)


        return solutions

    def get_path(self, state) -> List:
        n, q, *_, edge, prev = state

        if not prev:
            return [n]
        else:
            return self.get_path(prev) + [edge, n]

    def get_neighbors(self, n, q, A):
        # retrieve all the neighbours (n', q') of (n, q) in Gx
        # that is, look for a label "a" such that (n, a, n') is edge
        # and (q, a, q') is a transition in the automaton (using Automaton.delta)

        # get all the labels in the automaton
        labels = self.edge_trie.trie_map.keys()

        for label in labels:
            # get all the neighbors of n in G using label
            G_neighbors = self.query(label, n)

            for n_ in G_neighbors:
                # get neighbors from q in automaton with label

                for q_ in A.delta(q, label) or {}:
                    edge_ = (n, label, n_)
                    yield n_, q_, edge_



    def all_shortest_walk(self, v: int, regex: str) -> List:

        solutions = []
        A = Automaton(regex)
        open_list = []
        visited = {}

        if v in self.get_all_nodes():
            start_search_state = (v, A.start_state, 0, None)
            visited[(v, A.start_state)] = (0, None)
            open_list.append(start_search_state)

        while open_list:
            # BFS is mandatory here
            current = open_list.pop(BFS)
            n, q, depth, prev_list = current

            if A.is_final_state(current[1]):
                solutions.append(self.get_all_paths(current))

            for n_, q_, edge_ in self.get_neighbors(current[0], current[1], A):
                matching_state = visited.get((n_, q_))
                if matching_state:
                    depth_, prev_list_ = matching_state
                    if depth + 1 == depth_:
                        prev_list_.append((current, edge_))
                        # update matching state
                        visited[(n_, q_)] = (depth_, prev_list_)
                else:
                    prev_list = [(current, edge_)]
                    new_search_state = (n_, q_, depth+1, prev_list)
                    visited[(n_, q_)] = (depth+1, prev_list)
                    open_list.append(new_search_state)

        return solutions


    def get_all_paths(self, state):
        paths = []
        n, q, depth, prev_list = state
        if not prev_list:
            return [[n]]

        for prev_state, prev_edge in prev_list:
            for prev_path in self.get_all_paths(prev_state):
                paths.append(prev_path + [prev_edge, n])

        return paths


    def restricted_paths(
        self, v: int, regex: str, restrictor: str, selector: str = ""
    ) -> List:
        if selector not in ["all_shortest", "", "any", "any_shortest"]:
            raise ValueError("selector must be one of '', 'all_shortest', 'any', 'any_shortest'")
        if restrictor not in ["acyclic", "simple", "trail"]:
            raise ValueError("restrictor must be one of 'acyclic', 'simple', 'trail'")

        solutions = []
        A = Automaton(regex)
        open_list = []
        visited = set()
        reached_final = {}
        start_search_state = (v, A.start_state, 0, None, None)
        visited.add(start_search_state)
        open_list.append(start_search_state)

        if v in self.get_all_nodes() and A.start_state in A.final_states:
            reached_final[v] = 0
            solutions.append([v])

        search_type_selector = BFS if "shortest" in selector else DFS
        while open_list:
            current = open_list.pop(search_type_selector)
            n, q, depth, edge, prev = current
            for next_ in self.get_neighbors(n, q, A):
                n_, q_, edge_ = next_
                if self.is_valid(current, next_, restrictor):
                    new_search_state = (n_, q_, depth+1, edge_, current)
                    visited.add(new_search_state)
                    open_list.append(new_search_state)

                    if q_ in A.final_states:
                        path = self.get_path(new_search_state)
                        if selector in ["", "all_shortest"]:
                            if selector == "":
                                solutions.append(path)
                            elif n_ not in reached_final:
                                reached_final[n_] = depth + 1
                                solutions.append(path)
                            else:
                                optimal = reached_final[n_]
                                if depth + 1 == optimal:
                                    solutions.append(path)
                        else:
                            if n_ not in reached_final:
                                reached_final[n_] = -1
                                solutions.append(path)

        return solutions

    def is_valid(self, state, next_, restrictor):
        s = state
        while s:
            if restrictor == "acyclic":
                if s[0] == next_[0]:
                    return False
            elif restrictor == "simple":
                if s[0] == next_[0] and s[-1]:
                    return False
            elif restrictor == "trail":
                if s[3] == next_[2]:
                    return False
            s = s[-1]
        return True





















































