from typing import Set, Tuple, Dict
from time import sleep
from os import system, name
from tape import Tape, Direction


TransitionFunction = Dict[str, Dict[str, Tuple[str, str, Direction]]]


class TuringMachine:
    """Represents the Turing Machine
    """

    def __init__(self,
                 states: Set[str],
                 input_alphabet: Set[str],
                 acc_states: Set[str],
                 rej_states: Set[str] = set(),
                 transition_function: TransitionFunction = {},
                 tape: Tape = Tape(),
                 initial_state: str = "init",
                 start_symbol: str = ">",
                 empty_symbol: str = "") -> None:
        self.states = states
        self.input_alphabet = input_alphabet
        self.acc_states = acc_states
        self.rej_states = rej_states
        self.transition_function = transition_function
        self.initial_state = initial_state
        self.start_symbol = start_symbol
        self.empty_symbol = empty_symbol
        self.tape = tape

        # After exceeding max_steps value, the turing machine will be considered as looping.
        # Change this value for more complex scenarios.
        self.max_steps = 100

    def get_transition(self, state: str, read: str) -> Tuple[str, str, Direction]:
        return self.transition_function.get(state, {}).get(read, None)

    def add_state(self,
                  state: str,
                  is_acc: bool = False,
                  is_rej: bool = False) -> bool:
        """Adds state to the machine.

        Args:
            state (str): State to be added.
            is_acc (bool, optional): True if the state is accepting. Defaults to False.
            is_rej (bool, optional): True if the state is rejecting. Defaults to False.

        Returns:
            bool: False if the state is already present or 'is_acc' and 'is_rej' arguments are both True.
                  True otherwise.
        """
        if state in self.states or (is_acc and is_rej):
            return False

        if is_acc:
            self.acc_states.add(state)

        if is_rej:
            self.rej_states.add(state)

        return True

    def remove_state(self, state: str) -> bool:
        """
        Removes the state from the machine.

        Args:
            state (str): State to be removed.

        Returns:
            bool: Returns True if the state was added successfully, False otherwise.
        """
        if state not in self.states:
            return False

        if state in self.acc_states:
            self.acc_states.remove(state)

        if state in self.rej_states:
            self.rej_states.remove(state)

        self.states.remove(state)

        for state in self.transition_function:
            if state in self.transition_function.keys():
                del self.transition_function[state]

            for read in self.transition_function[state]:
                next_s, _, _ = self.transition_function[state][read]
                if next_s == state:
                    del self.transition_function[state][read]

        return True

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
        steps: int = 1
        output_file = None

        def clear_console() -> None:
            if name == "posix":
                system("clear")
            else:
                system("cls")

        def print_automaton_state() -> None:
            row = self.get_transition(state, self.tape.current.value)
            rule_str = f"{steps if row else steps - 1}. {(state, self.tape.current.value)} -> {row}\n"

            if output_file:
                output_file.write(rule_str)
                output_file.write(repr(self.tape))
                output_file.write(f"\n{'=' * 40}\n\n")

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
            self.tape.current.value = write
            self.tape.move(direction)

        close()

        print(f"Exceeded the maximum allowed steps. ({self.max_steps})")
        print("You change the default value by setting the 'max_steps' property of this automaton.")

        return False


if __name__ == "__main__":
    pass
