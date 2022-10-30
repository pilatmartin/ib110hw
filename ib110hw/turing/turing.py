from enum import Enum
from typing import Dict, Set, Tuple


class Direction(Enum):
    STAY = 0
    LEFT = 1
    RIGHT = 2


TransitionFunction = Dict[Tuple[str, str], Tuple[str, str, Direction, str]]


class Cell:

    def __init__(self,
                 value: str = "",
                 right: 'Cell' = None,
                 left: 'Cell' = None) -> None:
        self.value = value
        self.left = left
        self.right = right


class Tape():

    def __init__(self, start: Cell = None):
        self.start = start
        self.current = start

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

        while self.current is not start:
            self.move_left()

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
                 rej_states: Set[str] = [],
                 transition_function: TransitionFunction = {},
                 tape: Tape = Tape(),
                 start_symbol: str = ">",
                 empty_symbol: str = "") -> None:

        assert start_symbol != empty_symbol, "Start symbol cannot equal the empty symbol"
        assert not input_alphabet, "Input alphabet cannot be empty"
        assert acc_states.isdisjoint(
            rej_states
        ), "State cannot be accepting and rejecting at the same time"

        self.states = states
        self.input_alphabet = input_alphabet
        self.acc_states = acc_states
        self.rej_states = rej_states
        self.transition_function = transition_function
        self.start_symbol = start_symbol
        self.empty_symbol = empty_symbol
        self.tape = tape

    def simulate(self, path: str = "simulation.txt") -> None:
        raise NotImplemented()


if __name__ == "__main__":
    fn: TransitionFunction = {
        ("init", ">"): ("go", ">", Direction.RIGHT),
        ("go", "a"): ("init", "b", Direction.RIGHT),
        ("go", "b"): ("go", "b", Direction.RIGHT),
        ("go", ""): ("fin", "", Direction.STAY)
    }
    pass
