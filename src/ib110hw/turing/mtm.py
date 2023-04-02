from copy import deepcopy
from os import name, system
from time import sleep
from typing import Dict, List, Optional, Set, Tuple

from .base import BaseTuringMachine, MAX_STEPS_ERROR_MSG
from .tape import Direction, Tape

Symbols = Tuple[str, ...]
Directions = Tuple[Direction, ...]

MTMRule = Tuple[str, Symbols, Directions]
MTMRules = Dict[Symbols, MTMRule]
MTMTransitions = Dict[str, MTMRules]


class MTM(BaseTuringMachine):
    """
    Represents a Multi-tape Turing Machine
    """

    def __init__(
        self,
        states: Set[str],
        input_alphabet: Set[str],
        acc_states: Set[str],
        rej_states: Set[str] = set(),
        transitions: MTMTransitions = None,
        tape_count: int = 2,
        tapes: List[Tape] = None,
        initial_state: str = "init",
        start_symbol: str = ">",
    ):
        if transitions is None:
            transitions = {}
        super().__init__(
            states,
            input_alphabet,
            acc_states,
            rej_states,
            initial_state,
            start_symbol,
        )
        self.transitions = transitions
        self.tapes = tapes or [deepcopy(Tape()) for _ in range(tape_count)]
        self.tape_count = tape_count or len(tapes)

    def get_transition(self, state: str, read: Symbols) -> Optional[MTMRule]:
        """
        Returns the transition based on the current current state and read symbols.

        Args:
            state (str): Current state.
            read (Symbols): Current read symbols.

        Returns:
            Optional[MTMRule]: Transition based on the provided params if exists, None otherwise.
        """
        return self.transitions.get(state, {}).get(read, None)

    def write_to_tape(self, input_str: str, index: int = 0) -> None:
        """
        Writes the provided string on the tape on the index.

        Args:
            input_str (str): String to be written on the tape.
            index (int, optional): Index of the tape to be updated. Defaults to 0.
        """
        self.tapes[index].write(self.start_symbol + input_str)

    def clear_tape(self, index: int) -> None:
        """
        Clears the tape on the index.

        Args:
            index (int): Index of the tape.
        """
        self.tapes[index].clear()

    def clear_tapes(self) -> None:
        """
        Clears all the tapes
        """
        for tape in self.tapes:
            tape.clear()

    def get_current_symbols(self) -> Symbols:
        """
        Gets the current symbols read by tape heads.

        Returns:
            Symbols: Symbols read by the tape heads.
        """
        return tuple((tape.current.value for tape in self.tapes))

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

        def close():
            if output_file:
                output_file.close()

        def get_rule_string() -> str:
            row = self.get_transition(state, self.get_current_symbols())
            step_index = steps if row else steps - 1
            next_step = f"{state}, {self.get_current_symbols()}"

            return f"{step_index}. ({next_step}) -> {row}\n"

        def print_machine_configuration() -> None:
            rule_str = get_rule_string()

            if output_file:
                output_file.write(rule_str)

                for tape in self.tapes:
                    output_file.write(repr(tape))

                output_file.write(step_separator)

            if to_console:
                clear_console()
                print(rule_str, "\n\n")

                for i, tape in enumerate(self.tapes):
                    print(f"Tape {i}\n{repr(tape)}")

                sleep(delay)

        # the simulation itself starts here
        if to_file:
            output_file = open(path, "w")

        while steps <= (self.max_steps + 1):
            print_machine_configuration()

            if state in self.acc_states:
                close()
                return True

            read_symbols = self.get_current_symbols()
            rule = self.get_transition(state, read_symbols)

            if not rule or rule[0] in self.rej_states:
                close()
                return False

            steps += 1
            state, write, directions = rule

            for direction, tape, symbol in zip(directions, self.tapes, write):
                tape.write_symbol(symbol)
                tape.move(direction)

        close()
        print(MAX_STEPS_ERROR_MSG.format(self.max_steps))

        return False


if __name__ == "__main__":
    pass
