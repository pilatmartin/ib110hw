from typing import Set


class FA:
    """
    Finite Automaton
    """

    def __init__(self, states: Set[str], alphabet: Set[str],
                 initial_state: str, final_states: Set[str]):
        assert initial_state in states
        assert final_states.issubset(states)

        self.states = states
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.final_states = final_states

    def add_state(self, state: str, is_final: bool = False) -> bool:
        if (state in self.states):
            return False

        if is_final:
            self.final_states.add(state)

        self.states.add(state)
        return True

    def remove_state(self, state) -> bool:
        if state == self.initial_state or state not in self.states:
            return False

        if state in self.final_states:
            self.final_states.remove(state)

        self.states.remove(state)
        return True
