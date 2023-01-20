from typing import Set, Literal


class FA:
    """
    Finite Automaton
    """

    def __init__(self, states: Set[str], alphabet: Set[str],
                 initial_state: str, final_states: Set[str]) -> None:
        self.states = states
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.final_states = final_states

    def __assert_valid_states__(self):
        assert len(self.states) > 0, "Automaton has to have at least one state"
        assert self.initial_state in self.states, "The initial state has to be a part of the states set"
        assert self.final_states.issubset(
            self.states), "All final states have to be part of the states set"

    def __repr__(self) -> str:
        alphabet_str = ",".join(self.alphabet)
        states_str = ",".join(self.states)
        final_states_str = ",".join(self.final_states)

        return f"alphabet: {alphabet_str}\nstates: {states_str}\nfinal states: {final_states_str}\n"

    def __repr_transitions__(self, automaton_type: Literal["DFA",
                                                           "NFA"]) -> str:
        def get_row_prefix(state: str):
            if state == self.initial_state and state in self.final_states:
                return "<-> "
            if state == self.initial_state:
                return "--> "
            elif state in self.final_states:
                return "<-- "

            return "    "

        def get_max_cell_width():
            max_cell_width = 5

            for t in self.transitions.values():
                for next_val in t.values():
                    width = len(next_val) if automaton_type == "DFA" else len(
                        f"{{','.join(sorted(next_val))}}")
                    max_cell_width = max(max_cell_width, width)

            # add 4 for spaces on both sides
            return max_cell_width + 4

        cell_width = get_max_cell_width()
        header = f"{automaton_type : ^10}|"
        for letter in sorted(self.alphabet):
            header += f"{letter if letter else 'ε': ^{cell_width}}|"

        rows = ""
        for state in sorted(self.states):
            row_prefix = get_row_prefix(state)
            rows += f"{row_prefix: ^5}{state or 'empty': <5}"

            for letter in sorted(self.alphabet):
                transition = self.get_transition(state, letter)
                transition_str = transition if automaton_type == "DFA" else "{" + ",".join(
                    transition) + "}"
                rows += f"|{transition_str or 'empty': ^{cell_width}}"

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
        if state == self.initial_state or state not in self.states or len(
                self.states) == 1:
            return False

        if state in self.final_states:
            self.final_states.remove(state)

        self.states.remove(state)
        return True


if __name__ == "__main__":
    pass
