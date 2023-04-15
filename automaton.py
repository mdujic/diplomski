from typing import Dict, List, Set, Tuple
from collections import deque

from regex2nfa import regex_to_nfa

class Automaton:
    def __init__(self, regex: str):
        self.states = set()  # Set of states
        self.start_state = None  # Start state
        self.final_states = set()  # Set of final states
        self.alphabet = set()  # Set of alphabet symbols
        self.transitions = {}  # Dictionary containing transitions

        # Build automaton
        self._build_automaton(regex)

    def _build_automaton(self, regex: str) -> None:
        nfa = regex_to_nfa(regex)

        self.states = set(nfa["states"])
        self.start_state = nfa["initial_state"]
        self.final_states = set(nfa["final_states"])
        self.alphabet = set(nfa["alphabets"])
        self.transitions = nfa["transition_function"]

    def delta(self, q, a):
        if q in self.transitions and a in self.transitions[q]:
            return self.transitions[q][a]

    def is_final_state(self, q):
        return q in self.final_states

    def is_initial_state(self, q):
        return q == self.start_state

    def get_initial_state(self):
        return self.start_state

    def get_final_states(self):
        return self.final_states