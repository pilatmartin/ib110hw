from typing import Set


class FA:
    """
    Finite Automaton
    """

    def __init__(self, states: Set[str], alphabet: Set[str],
                 initial_state: str, final_states: Set[str]) -> None:
        assert len(states) > 0, "Automaton has to have at least one state"
        assert initial_state in states, "The initial state has to be a part of the states set"
        assert final_states.issubset(
            states), "All final states have to be part of the states set"

        self.states = states
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.final_states = final_states

    def __repr__(self) -> str:
        alphabet_str = ",".join(self.alphabet)
        states_str = ",".join(self.states)
        final_states_str = ",".join(self.final_states)

        return f"alphabet: {alphabet_str}\nstates: {states_str}\nfinal states: {final_states_str}\n"

    def __repr_transitions__(self, automaton_type: str) -> str:
        def get_row_prefix(state):
            if state == self.initial_state:
                return "-> "
            elif state in self.final_states:
                return "<- "

            return "   "

        header = f"{automaton_type: ^20}|"
        for letter in sorted(self.alphabet):
            header += f"{letter if letter else 'ε': ^20}|"

        rows = ""
        for state in sorted(self.states):
            row_prefix = get_row_prefix(state)
            rows += f"{row_prefix}{state or 'empty': <17}"

            for letter in sorted(self.alphabet):
                transition = self.get_transition(state, letter)
                transition_str = transition if automaton_type == "DFA" else "{" + ",".join(transition) + "}"
                rows += f"|{transition_str or 'empty': ^20}"

            rows += "\n"

        divider = "-" * rows.index("\n")

        return "\n".join([header[:-1], divider, rows])

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
        if state == self.initial_state or state not in self.states or len(self.states) == 1:
            return False

        if state in self.final_states:
            self.final_states.remove(state)

        self.states.remove(state)
        return True


if __name__ == "__main__":
    pass
