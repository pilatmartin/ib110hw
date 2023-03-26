from os import name, system
from time import sleep
from typing import Dict, Set, Tuple

from .base import BaseTuringMachine
from .tape import Direction, Tape

DTMRule = Tuple[str, str, Direction]
DTMRules = Dict[str, DTMRule]
DTMTransitions = Dict[str, DTMRules]


class DTM(BaseTuringMachine):
    """Represents a DETERMINISTIC Turing Machine"""

    def __init__(
        self,
        states: Set[str],
        input_alphabet: Set[str],
        acc_states: Set[str],
        rej_states: Set[str] = set(),
        transitions: DTMTransitions = None,
        tape: Tape = Tape(),
        initial_state: str = "init",
        start_symbol: str = ">",
        empty_symbol: str = "",
    ) -> None:
        if transitions is None:
            transitions = {}
        super().__init__(
            states,
            acc_states,
            rej_states,
            initial_state,
            start_symbol,
            empty_symbol,
        )
        self.input_alphabet = input_alphabet
        self.transitions = transitions
        self.tape = tape

    def get_transition(self, state: str, read: str) -> DTMRule:
        return self.transitions.get(state, {}).get(read, None)

    def remove_state(self, state: str) -> bool:
        if not super().remove_state(state):
            return False

        for state in self.transitions:
            if state in self.transitions.keys():
                del self.transitions[state]

            for read in self.transitions[state]:
                next_s, _, _ = self.transitions[state][read]
                if next_s == state:
                    del self.transitions[state][read]

        return True

    def write(self, input_str: str) -> None:
        self.tape.write(input_str)

    def clear_tape(self) -> None:
        self.tape.clear()

    def simulate(
        self,
        to_console: bool = True,
        to_file: bool = False,
        path: str = "simulation.txt",
        delay: float = 0.5,
    ) -> bool:
        """Simulates the machine on its current tape configuration.

        Args:
            to_console (bool, optional): Set to False if you only want to see the result. Defaults to True.
            to_file (bool, optional): Set to True if you want to save every step to the file. Defaults to False.
            path (str, optional): Path to the file with the step history. Defaults to "simulation.txt".
            delay (float, optional): The delay (s) between each step when printing to console. Defaults to 0.5.

        Returns:
            bool: False if the machine rejects the word or exceeds the 'max_steps' value, True otherwise.
        """
        state: str = self.initial_state
        steps: int = 1
        output_file = None
        step_separator = f"\n{'=' * 40}\n\n"

        def clear_console() -> None:
            if name == "posix":
                system("clear")
            else:
                system("cls")

        def get_rule_string() -> str:
            row = self.get_transition(state, self.tape.current.value)
            step_index = steps if row else steps - 1
            next_step = f"{state}, {self.tape.current.value}"

            return f"{step_index}. ({next_step}) -> {row}\n"

        def print_automaton_state() -> None:
            rule_str = get_rule_string()

            if output_file:
                output_file.write(rule_str)
                output_file.write(repr(self.tape))
                output_file.write(step_separator)

            if to_console:
                clear_console()
                print(rule_str, "\n", self.tape)

                sleep(delay)

        def close():
            print_automaton_state()

            if output_file:
                output_file.close()

        if to_file:
            output_file = open(path, "w")

        while steps <= self.max_steps:
            print_automaton_state()
            if state in self.acc_states:
                close()
                return True

            rule = self.get_transition(state, self.tape.current.value)

            if not rule or rule[0] in self.rej_states:
                close()
                return False

            steps += 1
            state, write, direction = rule
            self.tape.write_symbol(write)
            self.tape.move(direction)

        close()

        print(f"Exceeded the maximum allowed steps. ({self.max_steps})")
        print(
            "You change the default value by setting the 'max_steps' property of this automaton."
        )

        return False


if __name__ == "__main__":
    pass
