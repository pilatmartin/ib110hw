from typing import Dict, Set, Optional
from .fa import FA

DFATransitions = Dict[str, Dict[str, str]]


class DFA(FA):
    """
    Deterministic Finite Automaton.
    """

    def __init__(self, states: Set[str], alphabet: Set[str],
                 initial_state: str, final_states: Set[str],
                 transitions: DFATransitions):
        self.transitions = transitions

        super().__init__(states, alphabet, initial_state, final_states)

    def __assert_valid_alphabet__(self):
        assert "" not in self.alphabet, "DFAs alphabet cannot contain empty symbol (ε)."

    def __assert_valid_transition_function__(self):
        assert set(self.transitions.keys())\
            .issubset(self.states), \
            "All states in the transitions have to be part of the 'states' set."

        assert set().union(
            *[{*self.transitions[k].keys()} for k in self.transitions.keys()])\
            .issubset(self.alphabet), \
            "All symbols in the transition function have to be part of the alphabet."

        assert all([
            len(self.transitions[k].keys()) == len(self.alphabet)
            for k in self.transitions.keys()
        ]), "The transition function has to be complete."

    def __repr__(self) -> str:
        return super().__repr__() + "\n" + self.__repr_transitions__("DFA")

    def get_transition(self, state_from: str, symbol: str) -> str:
        """Returns next state from the provided state by symbol.

        Args:
            state_from (str): _description_
            symbol (str): _description_

        Returns:
            str: Next state if such transition exists, None otherwise.
        """
        return self.transitions.get(state_from, {}).get(symbol, None)

    def set_transition(self, state_from: str, state_to: str,
                       symbol: str) -> bool:
        """
        Adds/changes transition to automaton. And returns bool value based on success.
        If the automaton already contains transition from 'state_from' by 'symbol', it will be overwritten.

        Args:
            state_from (_type_): State name where the transition starts.
            state_to (_type_): State name where the transition ends.
            symbol (_type_): Transition symbol.

        Returns:
            bool: True if transition was added, False otherwise.
        """
        if not {state_from, state_to}.issubset(
                self.states) or not symbol or symbol not in self.alphabet:
            return False

        if not self.transitions[state_from]:
            self.transitions[state_from] = {symbol: state_to}
        else:
            self.transitions[state_from][symbol] = state_to

        return True

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
        if not {state_from, state_to}.issubset(
                self.states) or not symbol or symbol not in self.alphabet:
            return False

        if not self.get_transition(state_from, symbol):
            if state_from not in self.transitions.keys():
                self.transitions[state_from] = {}

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
        if self.get_transition(state_from, symbol):
            del self.transitions[state_from][symbol]
            return True

        return False

    def get_symbols_between_states(self, state_from: str, state_to: str) -> Set[str]:
        """
        Returns set of symbols between two states.
        Args:
            state_from: State name where the transition starts.
            state_to: State name where the transition ends.

        Returns:
            Set of symbols.
        """
        return set(
            [
                s for s in self.transitions[state_from].keys()
                if self.get_transition(state_from, s) == state_to
            ]
        )

    def add_state(self, state: str, is_final: bool = False) -> bool:
        """
        Adds a state to the automaton.

        Args:
            state (str): Name of the state to be added.
            is_final (bool, optional): Whether to mark the state as final. Defaults to False.

        Returns:
            bool: True if automaton did not contain such state, False otherwise.
        """
        return super().add_state(state, is_final)

    def remove_state(self, state) -> bool:
        """
        Removes the provided state from the automaton (from its states and transitions).

        Args:
            state (str): State to be removed.
        
        Returns:
            bool: True if automaton contained such state, False otherwise.
        """

        if not super().remove_state(state):
            return False

        self.transitions.pop(state, None)

        for s in self.states:
            if s not in self.transitions.keys():
                continue

            for symbol in list(self.transitions[s]):
                if self.transitions[s][symbol] == state:
                    del self.transitions[s][symbol]

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
            if not self.get_transition(current_state, c):
                return False

            current_state = self.transitions[current_state][c]

        return current_state in self.final_states


if __name__ == "__main__":
    pass
