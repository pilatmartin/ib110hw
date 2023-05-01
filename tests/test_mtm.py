from hypothesis import given
from sys import path
from generation import acc_palindromes, rej_palindromes

path.append("../src/ib110hw")
from turing.mtm import MTM
from turing.tape import Direction


PALINDROME_MACHINE: MTM = MTM(
    states={"init", "goToEnd", "goToStart", "check", "accept", "reject"},
    initial_state="init",
    input_alphabet={"a", "b"},
    acc_state="accept",
    rej_state="reject",
    transitions={
        "init": {(">", ""): ("copy", (">", ""), (Direction.RIGHT, Direction.STAY))},
        "copy": {
            ("a", ""): ("copy", ("a", "a"), (Direction.RIGHT, Direction.RIGHT)),
            ("b", ""): ("copy", ("b", "b"), (Direction.RIGHT, Direction.RIGHT)),
            ("", ""): ("goToStart", ("", ""), (Direction.LEFT, Direction.STAY)),
        },
        "goToStart": {
            ("a", ""): ("goToStart", ("a", ""), (Direction.LEFT, Direction.STAY)),
            ("b", ""): ("goToStart", ("b", ""), (Direction.LEFT, Direction.STAY)),
            (">", ""): ("check", (">", ""), (Direction.RIGHT, Direction.LEFT)),
        },
        "check": {
            ("a", "a"): ("check", ("a", "a"), (Direction.RIGHT, Direction.LEFT)),
            ("b", "b"): ("check", ("b", "b"), (Direction.RIGHT, Direction.LEFT)),
            ("", ""): ("accept", ("", ""), (Direction.STAY, Direction.STAY)),
            ("a", "b"): ("reject", ("a", "b"), (Direction.STAY, Direction.STAY)),
            ("b", "a"): ("reject", ("b", "a"), (Direction.STAY, Direction.STAY)),
        },
    },
)

PALINDROME_MACHINE.max_steps = 10000


@given(acc_palindromes())
def test_simulate_acc(input_str: str):
    PALINDROME_MACHINE.write_to_tape(input_str)
    assert PALINDROME_MACHINE.simulate(to_console=False)
    PALINDROME_MACHINE.clear_tapes()


@given(rej_palindromes())
def test_simulate_rej(input_str: str):
    PALINDROME_MACHINE.write_to_tape(input_str)
    assert not PALINDROME_MACHINE.simulate(to_console=False)
    PALINDROME_MACHINE.clear_tapes()
