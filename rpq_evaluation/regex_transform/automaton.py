from FAdo.fa import *
from FAdo.reex import *
from FAdo.fio import *

class Automaton:
    def __init__(self, regex: str):

        # Build automaton
        self._build_automaton(regex)

    def _build_automaton(self, regex: str) -> None:
        r = str2regexp(regex)
        # we don't want epsilon transitions
        nfa = r.nfaGlushkov()

        self.states = [*range(len(nfa.States))]
        self.start_state = next(iter(nfa.Initial))
        self.final_states = nfa.Final
        self.alphabet = nfa.Sigma
        self.transitions = nfa.delta

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
