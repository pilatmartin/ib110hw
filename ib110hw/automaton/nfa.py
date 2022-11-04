from typing import Dict, Set, Optional
from .fa import FA
from copy import deepcopy

NFARule = Dict[str, Set[str]]
NFATransitions = Dict[str, NFARule]


class NFA(FA):
    """
    Nondeterministic Finite Automaton
    """

    def __init__(self,
                 states: Set[str],
                 alphabet: Set[str],
                 initial_state: str,
                 final_states: Set[str],
                 transitions: Optional[NFATransitions] = {}):
        super().__init__(states, alphabet, initial_state, final_states)
        assert set(transitions.keys()).issubset(states)
        self.transitions = transitions

    def __eq__(self, other: object) -> bool:
        """
        Compares two NFAs. Automatons are equal when they accept the same language.

        Args:
            other (object): Object to compare the NFA with.

        Returns:
            bool: True if automatons are equal, False otherwise.
        """
        raise NotImplemented()

    def add_transition(self, state_from: str, state_to: str,
                       symbol: str) -> bool:
        """
        Adds transition to the automaton and returns bool based on success.

        Args:
            state_from (str): _description_
            state_to (str): _description_
            symbol (str): _description_
        
        Returns:
            bool: True if transition was successfuly added, False otherwise.
        """
        if not {state_from, state_to}.issubset(self.states):
            return False

        if not self.transitions[state_from][symbol]:
            self.transitions[state_from][symbol] = set()

        if state_to in self.transitions[state_from][symbol]:
            return False

        self.transitions[state_from][symbol].add(state_to)
        return True

    def remove_transition(self, state_from: str, state_to: str,
                          symbol: str) -> bool:
        """
        Adds transition to the automaton and returns bool based on success.

        Args:
            state_from (str): _description_
            state_to (str): _description_
            symbol (str): _description_

        Returns:
            bool: True if transition was successfully added, False otherwise
        """
        if not self.transitions[state_from] or not self.transitions[
                state_from][symbol]:
            return False

        del self.transitions[state_from][state_to]
        return True

    def add_state(self, state: bool, is_final: bool = False) -> bool:
        if (super.add_state(state, is_final)):
            self.transitions[state] = {}
            return True

        return False

    def remove_state(self, state) -> None:
        """
        Removes provided state from the automaton (from its states and transitions)

        Args:
            automaton (Union[NFA, DFA]): automaton to be updated
            state (str): state to be removed
        """
        if not super.remove_state(state):
            return False

        for s in self.states:
            rules = self.transitions[s]
            all_states = set().union(*rules.values())

            if (state not in all_states):
                continue

            rules[{k for k in rules.keys() if state in rules[k]}].remove(state)

        return True

    def is_accepted(self, word: str) -> bool:
        """
        Checks whether the provided word is accepted by the automaton.

        Args:
            word (str): Word to be tested.

        Returns:
            bool: True if word is accepted, False otherwise.
        """
        def is_accepted_rec(self, automaton: 'NFA', current_state: str, word: str) -> bool:
            if not word:
                return current_state in automaton.final_states

            if not automaton.transitions[current_state][word[0]]:
                return False
            
            result = False

            for state in automaton.transitions[current_state][word[0]]:
                tmp = deepcopy(automaton)
                tmp.transitions[current_state][word[0]]
                result = result or self.__is_accepted_rec__(tmp, state, word[1:])

            return result

        return is_accepted_rec(deepcopy(self), self.initial_state, word)
            

