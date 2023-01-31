from typing import Dict, Set

from base import BaseFiniteAutomaton

NFARules = Dict[str, Set[str]]
NFATransitions = Dict[str, NFARules]


class NFA(BaseFiniteAutomaton):
    """
    Nondeterministic Finite Automaton
    """

    def __init__(
        self,
        states: Set[str],
        alphabet: Set[str],
        initial_state: str,
        final_states: Set[str],
        transitions: NFATransitions,
    ):
        super().__init__(states, alphabet, initial_state, final_states)

        self.transitions = transitions

    def __repr__(self) -> str:
        return super().__repr__() + "\n" + self.__repr_transitions__()

    def __repr_transitions__(self) -> str:
        def get_max_cell_width():
            max_cell_width = 5

            for key, value in self.transitions.items():
                for next_value in value.values():
                    width = len(",".join(sorted(next_value)))
                    max_cell_width = max(max_cell_width, width, len(key))

            # add 4 for spaces on both sides
            return max_cell_width + 4

        cell_width = get_max_cell_width()
        header = f"{'NFA': ^{cell_width+5}}|"
        for letter in sorted(self.alphabet):
            header += f"{letter or 'ε': ^{cell_width}}|"

        rows = ""
        for state in sorted(self.states):
            row_prefix = self.__repr_row_prefix__(state)
            rows += f"{row_prefix: ^5}{state or 'empty': <{cell_width}}"

            for letter in sorted(self.alphabet):
                transition = self.get_transition(state, letter)
                transition_str = "{" + ",".join(transition) + "}"
                rows += f"|{transition_str or 'empty': ^{cell_width}}"

            rows += "\n"

        divider = "-" * rows.index("\n")

        return "\n".join([header[:-1], divider, rows])

    def get_transition(self, state_from: str, symbol: str) -> Set[str]:
        """Returns next possible states from the provided state by symbol.

        Args:
            state_from (str): _description_
            symbol (str): _description_

        Returns:
            Set[str]: Set of next states.
        """
        return self.transitions.get(state_from, {}).get(symbol, set())

    def set_transition(self, state_from: str, states_to: Set[str], symbol: str) -> bool:
        """
        Adds/changes transition to automaton. And returns bool value based on success.
        If the automaton already contains transition from 'state_from' by 'symbol', it will be overwritten.

        Args:
            state_from (str): State name where the transition starts.
            states_to (Set[str]): States where the transition ends.
            symbol (str): Transition symbol.

        Returns:
            bool: True if transition was added, False otherwise.
        """
        if (
            not {state_from, *states_to}.issubset(self.states)
            or not symbol
            or symbol not in self.alphabet
        ):
            return False

        if not self.transitions[state_from]:
            self.transitions[state_from] = {symbol: states_to}
        else:
            self.transitions[state_from][symbol] = states_to

        return True

    def add_transition(self, state_from: str, states_to: Set[str], symbol: str) -> bool:
        """
        Adds transition to the automaton and returns bool based on success.

        Args:
            state_from (str): _description_
            states_to (Set[str]): _description_
            symbol (str): _description_

        Returns:
            bool: True if transition was successfully added, False otherwise.
        """
        if (
            not {state_from, *states_to}.issubset(self.states)
            or symbol not in self.alphabet
        ):
            return False

        if state_from not in self.transitions.keys():
            self.transitions[state_from] = {}

        transition = self.get_transition(state_from, symbol)

        if not transition:
            self.transitions[state_from][symbol] = set()

        if not states_to.difference(transition):
            return False

        self.transitions[state_from][symbol].update(states_to)

        return True

    def remove_transition(self, state_from: str, state_to: str, symbol: str) -> bool:
        """
        Adds transition to the automaton and returns bool based on success.

        Args:
            state_from (str): _description_
            state_to (str): _description_
            symbol (str): _description_

        Returns:
            bool: True if transition was successfully added, False otherwise
        """
        transition = self.get_transition(state_from, symbol)

        if not transition or state_to not in transition:
            return False

        self.transitions[state_from][symbol].remove(state_to)

        return True

    def get_symbols_between_states(self, state_from: str, state_to: str) -> Set[str]:
        """
        Returns set of symbols between two states.
        Args:
            state_from: State name where the transition starts.
            state_to: State name where the transition ends.

        Returns:
            Set of symbols.
        """
        return {
            s
            for s in self.transitions.get(state_from, {}).keys()
            if state_to in self.get_transition(state_from, s)
        }

    def add_state(self, state: str, is_final: bool = False) -> bool:
        return super().add_state(state, is_final)

    def remove_state(self, state: str) -> bool:
        """
        Removes provided state from the automaton (from its states and transitions)

        Args:
            state (str): state to be removed
        """
        if not super().remove_state(state):
            return False

        self.transitions.pop(state, None)

        for s in self.transitions.keys():
            rules = self.transitions[s]

            for k in rules.keys():
                rules[k] = rules[k].difference({state})

        return True

    def is_accepted(self, word: str) -> bool:
        """
        Checks whether the provided word is accepted by the automaton.

        Args:
            word (str): Word to be tested.

        Returns:
            bool: True if word is accepted, False otherwise.
        """

        def is_accepted_rec(current_state: str, curr_word: str) -> bool:
            if not curr_word:
                return current_state in self.final_states

            if not self.get_transition(current_state, curr_word[0]):
                return False

            result = False

            for state in self.get_transition(current_state, curr_word[0]):
                result = result or is_accepted_rec(state, curr_word[1:])

            return result

        return is_accepted_rec(self.initial_state, word)


if __name__ == "__main__":
    nfa_transitions: NFATransitions = {
        "s1": {
            "1": {"s2", "s4", "s3", "s5", "s6"},
            "0": {"s4"},
        },
        "s2": {
            "1": {"s3"},
        },
        "s4": {
            "0": {"s3"},
        },
    }

    automaton = NFA(
        states={"s1", "s2", "s3", "s4", "s5"},
        alphabet={"1", "0"},
        initial_state="s1",
        final_states={"s3"},
        transitions=nfa_transitions,
    )

    print(automaton)
