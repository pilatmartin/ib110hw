from typing import Dict, Set, Optional
from fa import FA

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
        Automatons are equal when they accept the same language.
        """
        # TODO
        return super().__eq__()

    def __repr__(self) -> str:
        # TODO
        return super().__repr__()

    def get_transition(self, state_from: str, symbol: str) -> Set[str]:
        """Returns next possible states from the provided state by symbol.

        Args:
            state_from (str): _description_
            symbol (str): _description_

        Returns:
            Set[str]: Set of next states.
        """
        if state_from not in self.transitions.keys() or \
            symbol not in self.transitions[state_from].keys():
            return set()

        return self.transitions[state_from][symbol]

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

        transition = self.get_transition(state_from, symbol)

        if not transition:
            self.transitions[state_from][symbol] = set()

        if state_to in transition:
            return False

        if state_from not in self.transitions.keys():
            self.transitions.add(state_from)

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
        if not self.get_transition(state_from, symbol):
            return False

        del self.transitions[state_from][state_to]

        return True

    def add_state(self, state: bool, is_final: bool = False) -> bool:
        if (super().add_state(state, is_final)):
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
        if not super().remove_state(state):
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

        def is_accepted_rec(current_state: str, word: str) -> bool:
            if not word:
                return current_state in self.final_states

            if not self.get_transition(current_state, word[0]):
                return False

            result = False

            for state in self.get_transition(current_state, word[0]):
                result = result or is_accepted_rec(state, word[1:])

            return result

        return is_accepted_rec(self.initial_state, word)



if __name__ == "__main__":
    transitions: NFATransitions = {
        "s1": {
            "a": {"s1", "s2"},
            "b": {"s1", "s3"},
            "c": {"s1", "s4"},
        },
        "s2": {
            "a": {"s2", "s5"},
            "b": {"s2"},
            "c": {"s2"},
        },
        "s3": {
            "a": {"s3"},
            "b": {"s3", "s5"},
            "c": {"s3"},
        },
        "s4": {
            "a": {"s4"},
            "b": {"s4"},
            "c": {"s4", "s5"},
        },
    }

    nfa = NFA({"s1", "s2", "s3", "s4", "s5"}, {"a", "b", "c"}, "s1", {"s5"},
              transitions)

    print(nfa.is_accepted("caba"))
