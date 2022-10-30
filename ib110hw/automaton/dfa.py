from typing import Dict, Set, Optional
from .fa import FA

DFARule = Dict[str, str]
DFATransitions = Dict[str, DFARule]


class DFA(FA):
    """
    Deterministic Finite Automaton
    """

    def __init__(self,
                 states: Set[str],
                 alphabet: Set[str],
                 initial_state: str,
                 final_states: Set[str],
                 transitions: Optional[DFATransitions] = {}):
        super().__init__(states, alphabet, initial_state, final_states)
        assert set(transitions.keys()).issubset(states)
        self.transitions = transitions

    def __eq__(self, other: object) -> bool:
        """
        Compares two DFAs. Automatons are equal when they accept the same language.

        Args:
            other (DFA): DFA to compare with

        Returns:
            bool: True if automatons are equal, False otherwise
        """
        raise NotImplemented()

    def __repr__(self) -> str:

        return super().__repr__()

    def add_transition(self, state_from: str, state_to: str,
                       symbol: str) -> bool:
        """
        Adds transition to automaton. And returns bool value based on success. 
        Nothing changes if the automaton already contains transition from 'state_from' by 'symbol'.

        Args:
            state_from (_type_): State name where the transition starts.
            state_to (_type_): State name where the transition ends.
            symbol (_type_): Transition symbol.

        Returns:
            bool: True if transition was added, False otherwise.
        """
        if not {state_from, state_to}.issubset(self.states):
            return False

        if not self.transitions[state_from][symbol]:
            self.transitions[state_from][symbol] = state_to
            return True

        return False

    def remove_transition(self, state_from: str, symbol: str) -> bool:
        """
        Removes transition from the automaton and returns bool based on success.

        Args:
            state_from (str): State name which the transition starts from.
            symbol (str): Transition symbol. 

        Returns:
            bool: True if the automaton contained such transition, False otherwise.
        """
        if self.transitions[state_from][symbol]:
            del self.transitions[state_from][symbol]
            return True

        return False

    def add_state(self, state: str, is_final: bool = False) -> bool:
        """
        Adds state to the automaton.

        Args:
            state (str): Name of the state to be added.
            is_final (bool, optional): Whether to mark the state as final. Defaults to False.

        Returns:
            bool: True if automaton did not contain such state, False otherwise.
        """
        return super().add_state(state, is_final)

    def remove_state(self, state) -> bool:
        """
        Removes provided state from the automaton (from its states and transitions).

        Args:
            state (str): State to be removed.
        
        Returns:
            bool: True if automaton contained such state, False otherwise.
        """

        if not super().remove_state(state):
            return False

        for s in self.states:
            rules = self.transitions[s].values()
            all_states = rules.values()

            if (state not in all_states):
                continue

            rules.pop({k for k in rules.keys() if rules[k] == state}, None)

        return True

    def is_accepted(self, word: str) -> bool:
        """
        Checks whether the provided word is accepted by the automaton.

        Args:
            word (str): Word to be tested.

        Returns:
            bool: True if word is accepted, False otherwise.
        """
        current_state = self.initial_state
        for c in word:
            if not self.transitions[current_state][c]:
                return False
            
            current_state = self.transitions[current_state][c]

        return current_state in self.final_states
