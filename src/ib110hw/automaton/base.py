from typing import Set


class BaseFiniteAutomaton:
    """
    Represents an abstract Finite Automaton class. This class cannot be instantiated.
    """

    def __new__(cls, *args, **kwargs):
        if cls is BaseFiniteAutomaton:
            raise TypeError("Only NFA and DFA can be instantiated!")

        return object.__new__(cls)

    def __init__(
        self,
        states: Set[str],
        alphabet: Set[str],
        initial_state: str,
        final_states: Set[str],
    ) -> None:
        self.states = states
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.final_states = final_states

    def __repr__(self) -> str:
        alphabet_str = ",".join(self.alphabet)
        states_str = ",".join(self.states)
        final_states_str = ",".join(self.final_states)

        return f"alphabet: {alphabet_str}\nstates: {states_str}\nfinal states: {final_states_str}\n"

    def __repr_row_prefix__(self, state: str):
        if state == self.initial_state and state in self.final_states:
            return "<-> "
        if state == self.initial_state:
            return "--> "
        elif state in self.final_states:
            return "<-- "

        return "    "

    def add_state(self, state: str, is_final: bool = False) -> bool:
        if state in self.states:
            return False

        if is_final:
            self.final_states.add(state)

        self.states.add(state)

        return True

    def remove_state(self, state) -> bool:
        # automaton would be without the initial state,
        # without states, or no such state exists
        if (
            state == self.initial_state
            or state not in self.states
            or len(self.states) == 1
        ):
            return False

        if state in self.final_states:
            self.final_states.remove(state)

        self.states.remove(state)
        return True


if __name__ == "__main__":
    pass
