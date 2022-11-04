from enum import Enum
from typing import Dict, Set, Tuple, List
from time import sleep
from os import system


class Direction(Enum):
    LEFT = -1
    STAY = 0
    RIGHT = 1

    def __repr__(self):
        return self.name


TransitionFunction = Dict[Tuple[str, str], Tuple[str, str, Direction]]


class Cell:

    def __init__(self,
                 value: str = "",
                 right: 'Cell' = None,
                 left: 'Cell' = None) -> None:
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return self.value if self.value else " "


class Tape():

    def __init__(self, start: Cell = Cell()):
        self.start = start
        self.current = start

    def __repr__(self) -> str:
        curr_cell: Cell = self.start

        # find the beggining of the tape
        while curr_cell.left:
            curr_cell = curr_cell.left

        cells: List[Cell] = []

        while curr_cell:
            cells.append(curr_cell)
            curr_cell = curr_cell.right

        str_cells = f"| {' | '.join([repr(c) for c in cells])} |\n"
        str_marker = f"{' ' * (2 + cells.index(self.current) * 4)}^\n"

        return str_cells + str_marker

    def move(self, direction: Direction) -> None:
        if direction == Direction.LEFT:
            self.move_left()
        elif direction == Direction.RIGHT:
            self.move_right()

    def move_left(self):
        if not self.current.left:
            self.current.left = Cell(right=self.current)

        self.current = self.current.left

    def move_right(self):
        if not self.current.right:
            self.current.right = Cell(left=self.current)

        self.current = self.current.right

    def write(self, text: str) -> None:
        start = self.current

        for symbol in text:
            self.current.value = symbol
            self.move_right()

        self.current = self.start

    def clear(self) -> None:
        self.start = Cell()
        self.current = self.start


class TuringMachine():
    """Represents Turing Machine
    """

    def __init__(self,
                 states: Set[str],
                 input_alphabet: Set[str],
                 acc_states: Set[str],
                 rej_states: Set[str] = set(),
                 transition_function: TransitionFunction = {},
                 tape: Tape = Tape(),
                 start_symbol: str = ">",
                 empty_symbol: str = "") -> None:

        assert start_symbol != empty_symbol, "Start and empty symbol cannot be the same."
        assert input_alphabet, "Input alphabet cannot be empty."
        assert acc_states.isdisjoint(
            rej_states
        ), "State cannot be accepting and rejecting at the same time."

        self.states = states
        self.input_alphabet = input_alphabet
        self.acc_states = acc_states
        self.rej_states = rej_states
        self.transition_function = transition_function
        self.start_symbol = start_symbol
        self.empty_symbol = empty_symbol
        self.tape = tape

        # After exceeding max_steps value, the turing machine will be considered as looping.
        # Change this value for more complex scenarios.
        self.max_steps = 100

    def add_state(self,
                  state: str,
                  is_acc: bool = False,
                  is_rej: bool = False) -> bool:
        if state in self.states or (is_acc and is_rej):
            return False

        if is_acc:
            self.acc_states.add(state)

        if is_rej:
            self.rej_states.add(state)

        return True

    def remove_state(self, state: str) -> bool:
        """
        Removes the state from the turing machine () 

        Args:
            state (str): State to be added.

        Returns:
            bool: Returns True if the state was added successfully, False otherwise.
        """
        if not state in self.states:
            return False

        if state in self.acc_states:
            self.acc_states.remove(state)

        if state in self.rej_states:
            self.rej_states.remove(state)

        self.states.remove(state)

        for key, value in self.transition_function:
            if key[0] == state or value[0] == state:
                del self.transition_function[key]

        return True

    def simulate(self,
                 to_console: bool = True,
                 to_file: bool = False,
                 path: str = "simulation.txt") -> bool:
        state: str = "init"
        write: str = self.start_symbol
        steps: int = 1
        output_file = None

        def print_automaton_state():
            row = self.transition_function.get((state, self.tape.current.value))
            rule_str = f"{steps if row else steps-1}. {(state, self.tape.current.value)} -> {row}\n"

            if output_file:
                output_file.write(rule_str)
                output_file.write(repr(self.tape))
                output_file.write(f"\n{'=' * 40}\n\n")

            if to_console:
                system("cls")
                print(rule_str)
                print(self.tape)

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

            rule = self.transition_function.get(
                (state, self.tape.current.value))

            if not rule or rule[0] in self.rej_states:
                close()
                return False

            steps += 1
            state, write, direction = rule
            self.tape.current.value = write
            self.tape.move(direction)

            sleep(.5)

        print(f"Exceeded the maximum steps allowed. ({self.max_steps})")
        print(
            "You change the default value by setting the 'max_steps' property of this automaton."
        )
        close()

        return False


if __name__ == "__main__":
    fn: TransitionFunction = {
        ("init", ">"): ("findA", ">", Direction.RIGHT),
        ("space", "a"): ("writeA", "", Direction.RIGHT),
        ("space", "b"): ("writeB", "", Direction.RIGHT),
        ("space", ""): ("finish", "c", Direction.STAY),
        ("writeA", "a"): ("writeA", "a", Direction.RIGHT),
        ("writeA", "b"): ("writeB", "a", Direction.RIGHT),
        ("writeA", ""): ("back", "a", Direction.STAY),
        ("writeB", "a"): ("writeA", "b", Direction.RIGHT),
        ("writeB", "b"): ("writeB", "b", Direction.RIGHT),
        ("writeB", ""): ("back", "b", Direction.STAY),
        ("findA", "a"): ("space", "c", Direction.RIGHT),
        ("findA", "b"): ("findA", "b", Direction.RIGHT),
        ("findA", ""): ("finish", "", Direction.STAY),
        ("back", "a"): ("back", "a", Direction.LEFT),
        ("back", "b"): ("back", "b", Direction.LEFT),
        ("back", ""): ("findA", "c", Direction.RIGHT),
    }

    tape_ = Tape()
    tape_.write(">abba")

    turing = TuringMachine(
        states={"init", "space", "writeA", "writeB", "findA", "back"},
        acc_states={"finish"},
        input_alphabet={"a", "b", "c"},
        tape=tape_,
        transition_function=fn)

    print(turing.simulate(to_file=True))
