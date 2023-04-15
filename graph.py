from typing import List, Tuple
from collections import deque

from trie import Trie
from automaton import Automaton


class Edge:
    def __init__(self, source: int, target: int, label: str):
        self.source = source
        self.target = target
        self.label = label

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

    def get_neighbors(self, v: int) -> List[int]:
        neighbors = []
        for label in self.edge_trie.trie_map.keys():
            neighbors += self.query(label, v)
        
        return neighbors

    def search(self, v: int) -> Tuple[List[int], List[Tuple[int, int, str]]]:
        # Initialize queue and visited set
        q = deque()
        visited = set()

        # Initialize start node
        start = v
        q.append(start)
        visited.add(start)

        # Initialize solutions list and paths dict
        solutions = [v]
        paths = {v: None}

        # BFS search
        while q:
            current = q.popleft()

            # Check neighbors with query call by all labels in edge_trie.trie_map.keys()
            neighbors = self.get_neighbors(current)
            for neighbor in neighbors:
                next_node = neighbor
                if next_node not in visited:
                    q.append(next_node)
                    visited.add(next_node)
                    paths[next_node] = current
                    if neighbor not in solutions:
                        solutions.append(neighbor)

        # Reconstruct paths
        paths_list = []
        for node in paths:
            if node != v:
                path = []
                current = node
                while current is not None:
                    path.append(current)
                    current = paths[current]
                path.reverse()
                paths_list.append(tuple(path))

        return solutions, paths_list

    def search_all_shortest_paths(self, start_node: int):
        open_list = []
        visited = {}
        start = (start_node, 0, None)
        open_list.append(start)
        visited[start_node] = start
        solutions = []
        while open_list:
            current = open_list.pop(0)
            node, depth, prev_list = current
            solutions.append(node)
            self.reconstruct_paths(current)
            neighbours = self.get_neighbors(node)
            for neighbour in neighbours:
                if neighbour not in visited.keys():
                    new = (neighbour, depth+1, [current])
                    open_list.append(new)
                    visited[neighbour] = new
                else:
                    existing = visited[neighbour]
                    if existing[1] == depth+1:
                        existing[2].append(current)

    def reconstruct_paths(self, current):
        node, depth, prev_list = current
        if prev_list is None:
            return
        for prev in prev_list:
            path = [node]
            while prev is not None:
                if len(prev) == 1:
                    prev = prev[0]
                path.append(prev[0])
                prev = prev[2]
            path.reverse()
            print("Path:", path)

    def rpq_eval(self, source: int, regex: str) -> List[int]:
        automaton = Automaton(regex)
        start = (source, automaton.start_state, None)
        open_list = [start]
        visited = set((source, automaton.start_state))
        solutions = set()
        while open_list:
            current = open_list.pop(0)
            if automaton.is_final_state(current[1]):
                solutions.add(current[0])
                self.reconstruct_path_rpq(current)
            neighbors = self.get_neighbors_rpq(current, automaton)
            for n, q in neighbors:
                if (n, q) not in visited:
                    next = (n, q, current)
                    open_list.append(next)
                    visited.add((n, q))
        return list(solutions)
    
    def reconstruct_path_rpq(self, current):
        node, state, prev = current
        path = [node]
        while prev is not None:
            if prev[0] != path[-1]:
                path.append(prev[0])
            prev = prev[2]
        path.reverse()
        print("Path:", path)

    def get_neighbors_rpq(self, current, automaton):
        n, q, prev = current
        # retrieve all the neighbours (n', q') of (n, q) in Gx
        # that is, look for a label "a" such that (n, a, n') is edge
        # and (q, a, q') is a transition in the automaton (using Automaton.delta)

        # get all the labels in the automaton
        labels = self.edge_trie.trie_map.keys()
        neighbors = []

        for label in labels:
            # get all the neighbors of n
            n_neighbors = self.query(label, n)
            
            for n_neighbor in n_neighbors:
                # get the transition from q to q' using label
                q_neighbors = automaton.delta(q, label)
                
                if q_neighbors:
                    for q_neighbor in q_neighbors:
                        neighbors.append((n_neighbor, q_neighbor))

        # also add the epsilon transitions
        # neighbors are all the nodes that are reachable from q using only epsilon transitions
        epsilon_neighbors = []

        stack = [q]
        visited = set()
        while stack:
            current = stack.pop()
            visited.add(current)
            epsilon_neighbors.append(current)
            for neighbor in automaton.delta(current, '$'):
                if neighbor not in visited:
                    stack.append(neighbor)
        
        for epsilon_neighbor in epsilon_neighbors:
            neighbors.append((n, epsilon_neighbor))
        
        return neighbors