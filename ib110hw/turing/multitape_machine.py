from typing import Set, Dict, Tuple, List
from time import sleep
from os import system, name

from machine import TuringMachine
from tape import Tape, Direction

MultitapeTransitions = Dict[int, Dict[str, Dict[int, Dict[str, Tuple[str, str, Direction]]]]]


class MTM(TuringMachine):
    """Represents a MULTI-TAPE Turing Machine"""

    def __init__(self,
                 states: Set[str],
                 input_alphabet: Set[str],
                 acc_states: Set[str],
                 rej_states: Set[str] = set(),
                 transition_function: MultitapeTransitions = {},
                 tapes: List[Tape] = [Tape()],
                 initial_state: str = "init",
                 start_symbol: str = ">",
                 empty_symbol: str = ""):
        super().__init__(states, input_alphabet, acc_states, rej_states, initial_state, start_symbol, empty_symbol)
        self.transition_function = transition_function
        self.tapes = tapes

    def get_transition(self, index: int, state: str, read: str) -> Tuple[str, str, Direction]:
        return self.transition_function.get(index, {}).get(state, {}).get(read, None)

    def simulate(self,
                 to_console: bool = True,
                 to_file: bool = False,
                 path: str = "simulation.txt",
                 delay: float = 0.5) -> bool:
        """ Simulates the machine on its current tape configuration.

        Args:
            to_console (bool, optional): Set to False if you only want to see the result. Defaults to True.
            to_file (bool, optional): Set to True if you want to save every step to the file. Defaults to False.
            path (str, optional): Path to the file with the step history. Defaults to "simulation.txt".
            delay (float, optional): The delay (s) between each step when printing to console. Defaults to 0.5.

        Returns:
            bool: False if the machine rejects the word or exceeds the 'max_steps' value, True otherwise.
        """
        state: str = self.initial_state
        tape_index: int = 0
        steps: int = 1
        output_file = None

        def clear_console() -> None:
            if name == "posix":
                system("clear")
            else:
                system("cls")

        def print_automaton_state() -> None:
            row = self.get_transition(tape_index, state, self.tapes[tape_index].current.value)
            rule_str = f"{steps if row else steps - 1}. {self.tapes[tape_index].current.value} -> {row}\n"

            if output_file:
                output_file.write(rule_str)

                for tape in self.tapes:
                    output_file.write(repr(tape))

                output_file.write(f"\n{'=' * 40}\n\n")

            if to_console:
                clear_console()
                print(rule_str, "\n")
                print("\n".join([repr(tape) for tape in self.tapes]))

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

            rule = self.get_transition(tape_index, state, self.tapes[tape_index].current.value)

            if not rule or rule[0] in self.rej_states:
                close()
                return False

            steps += 1
            state, write, direction = rule
            self.tapes[tape_index].current.value = write
            self.tapes[tape_index].move(direction)

        close()

        print(f"Exceeded the maximum allowed steps. ({self.max_steps})")
        print("You change the default value by setting the 'max_steps' property of this automaton.")

        return False


if __name__ == "__main__":
    idk: MultitapeTransitions = {
        0: {
            "init":
                {
                    0: {
                        ">": ("state", ">", Direction.RIGHT)
                    }
                }
        }
    }
