from enum import Enum
from typing import Dict, Set, Tuple, List
from time import sleep
from os import system, name


class Direction(Enum):
    LEFT = -1
    STAY = 0
    RIGHT = 1

    def __repr__(self):
        return self.name


TransitionFunction = Dict[str, Dict[str, Tuple[str, str, Direction]]]


class Cell:
    """Represents one cell of a Turing machine memory tape.
    """

    def __init__(self,
                 value: str = "",
                 right: 'Cell' = None,
                 left: 'Cell' = None) -> None:
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return self.value if self.value else " "


class Tape:
    """Represents Turing machine memory tape as a linked list.
    """

    def __init__(self, start: Cell = Cell()):
        self.start = start
        self.current = start

    def __repr__(self) -> str:
        curr_cell: Cell = self.start

        # find the leftmost cell
        while curr_cell.left:
            curr_cell = curr_cell.left

        cells: List[Cell] = []

        while curr_cell:
            cells.append(curr_cell)
            curr_cell = curr_cell.right

        # ['a', 'b'] -> | a | b |
        str_cells = f"| {' | '.join([repr(c) for c in cells])} |\n"

        # adds spaces to put the cursor '^' below the current cell
        str_cursor = f"{' ' * (2 + cells.index(self.current) * 4)}^\n"

        return str_cells + str_cursor

    def move(self, direction: Direction) -> None:
        """Moves the tape cursor based on the provided direction.

        Args:
            direction (Direction): Specifies the move direction.
        """
        if direction == Direction.LEFT:
            self.move_left()
        elif direction == Direction.RIGHT:
            self.move_right()

    def move_left(self):
        """Moves the tape cursor to the left. (current will be current.left)
        """
        if not self.current.left:
            self.current.left = Cell(right=self.current)

        self.current = self.current.left

    def move_right(self):
        """Moves the tape cursor to the right. (current will be current.right)
        """
        if not self.current.right:
            self.current.right = Cell(left=self.current)

        self.current = self.current.right

    def write(self, text: str) -> None:
        """Writes the provided text on the tape.

        Args:
            text (str): Text to be written on the tape.
        """
        for symbol in text:
            self.current.value = symbol
            self.move_right()

        self.current = self.start

    def clear(self) -> None:
        """Clears the tape contents and places the cursor on the start.
        """
        self.start = Cell()
        self.current = self.start


class TuringMachine:
    """Represents Turing Machine
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
    fn: TransitionFunction = {
        "init": {
            ">": ("findA", ">", Direction.RIGHT)
        },
        "space": {
            "a": ("writeA", "", Direction.RIGHT),
            "b": ("writeB", "", Direction.RIGHT),
            "": ("finish", "c", Direction.STAY),
        },
        "writeA": {
            "a": ("writeA", "a", Direction.RIGHT),
            "b": ("writeB", "a", Direction.RIGHT),
            "": ("back", "a", Direction.STAY),
        },
        "writeB": {
            "a": ("writeA", "b", Direction.RIGHT),
            "b": ("writeB", "b", Direction.RIGHT),
            "": ("back", "b", Direction.STAY),
        },
        "findA": {
            "a": ("space", "c", Direction.RIGHT),
            "b": ("findA", "b", Direction.RIGHT),
            "": ("finish", "", Direction.STAY),
        },
        "back": {
            "a": ("back", "a", Direction.LEFT),
            "b": ("back", "b", Direction.LEFT),
            "": ("findA", "c", Direction.RIGHT),
        }
    }

    tape_ = Tape()
    tape_.write(">aba")

    turing = TuringMachine(
        states={"init", "space", "writeA", "writeB", "findA", "back"},
        acc_states={"finish"},
        rej_states=set(),
        initial_state="init",
        input_alphabet={"a", "b", "c"},
        tape=tape_,
        transition_function=fn)

    print(turing.simulate(delay=.2), "\n")

    input("Press any key to continue")

    tape_.clear()
    tape_.write(">abbaaabababababaa")
    turing.max_steps = 200
    print(turing.simulate(delay=.05))
