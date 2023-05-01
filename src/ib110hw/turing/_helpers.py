from os import name, system
from typing import IO, List, Tuple, Set, Optional
from tape import Tape, Direction
from itertools import takewhile, dropwhile
from pynput import keyboard


def clear_console() -> None:
    if name == "posix":
        system("clear")
    else:
        system("cls")


def close_file(file: IO) -> None:
    if file:
        file.close()


# inspired by https://stackoverflow.com/a/43106497
def get_step_direction() -> str:
    step_direction = None
    print("Use arrow keys [L|R] to go back or forward. Esc to exit.")

    def on_press(key):
        nonlocal step_direction
        try:
            if key.name in ["left", "right", "esc"]:
                step_direction = key.name
                return False
        except AttributeError:
            # ignore other keys
            pass

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()
    return step_direction


def tape_to_md(tape: Tape, index: int = None) -> str:
    index_str = "" if index is None else f"<b>Tape {index}:</b>"
    tape_str = f"{tape}".replace("^", "<b>^</b>")
    return f"{index_str}\n{tape_str}\n"


def rule_to_md(rule_str: str) -> str:
    return f"######{rule_str.replace('->', '&rarr;')}"


def dtm_config_to_md(tape: Tape, rule_str: str) -> str:
    header_str = rule_to_md(rule_str)
    tape_str = tape_to_md(tape)

    return f"{header_str}\n<pre>\n{tape_str}</pre>\n---\n"


def mtm_config_to_md(tapes: List[Tape], rule_str: str) -> str:
    header_str = rule_to_md(rule_str)
    tapes_str = "".join(tape_to_md(tape, i) for i, tape in enumerate(tapes))

    return f"{header_str}\n<pre>\n{tapes_str}</pre>\n---\n"


def read_file(file_path: str) -> List[str]:
    result = []
    with open(file_path, "r") as in_file:
        for line in in_file:
            line = " ".join(line.split())

            if not line.strip() or line.startswith("#"):
                continue

            result.append(f"{line.strip()}")

    return result


def parse_direction(direction: str) -> Optional[Direction]:
    directions = {"L": -1, "R": 1, "S": 0}
    return Direction(directions.get(direction, 0))


def get_configuration(
    definition: List[str],
) -> Tuple[str, Set[str], Set[str], Set[str]]:
    config = list(takewhile(lambda l: l.strip() != "---", definition))[:-1]
    init = ""
    acc, rej, abc = set(), set(), set()

    for line in config:
        if line.startswith("init"):
            init = line.split()[1]
        elif line.startswith("acc"):
            acc = {*line.split()[1:]}
        elif line.startswith("rej"):
            rej = {*line.split()[1:]}
        elif line.startswith("alphabet"):
            abc = {*line.split()[1:]}

    return (init, acc or set(), rej or set(), abc or set())


def get_dtm_transition_function(definition: List[str]):
    function_lines = list(dropwhile(lambda l: l != "---", definition))[1:]
    function = {}

    for rule in function_lines:
        left, right = rule.split("->")
        curr_state, read = left.split()
        next_state, write, direction = right.split()

        if not function.get(curr_state):
            function[curr_state] = {}

        read = read if read != "_" else ""
        function[curr_state][read] = (next_state, write, parse_direction(direction))

    return function


def validate_configuration(definition: List[str]) -> Optional[str]:
    if all(l.strip() != "---" for l in definition):
        return "The divider is missing."

    config = list(takewhile(lambda l: l != "---", definition))[:-1]

    if not any((l.startswith("init") for l in config)):
        return "Specifying the initial state is mandatory."

    init_line = next((l for l in config if l.startswith("init")), None)
    if init_line:
        if len(init_line.split()) != 2:
            return "Invalid initial state"


def validate_dtm_transitions(definition: List[str]) -> Optional[str]:
    lines = list(dropwhile(lambda l: l != "---", definition))[1:]
    get_part = lambda l, i: l.split("->")[i]
    # checks the length of arguments on the left side
    valid_current = lambda l: len(get_part(l, 0).split()) == 2
    # checks the length of the read symbol
    valid_read = lambda l: len(get_part(l, 0).split()[1]) == 1
    # checks the length of arguments on the right side
    valid_next = lambda l: len(get_part(l, 1).split()) == 3
    # checks the length of the write symbol
    valid_write = lambda l: len(get_part(l, 1).split()[1]) == 1
    # checks the direction
    valid_dir = lambda l: get_part(l, 1).split()[-1] in ["L", "R", "S"]

    rule = next((l for l in lines if "->" not in l), None)
    if rule:
        return f"Missing arrow in rule:\n{rule}."

    rule = next((l for l in lines if not valid_current(l)), None)
    if rule:
        return f"Invalid combination of state and read symbol in rule:\n{rule}"

    rule = next((l for l in lines if not valid_read(l)), None)
    if rule:
        return f"Invalid read symbol length (> 1) in rule\n{rule}"

    rule = next((l for l in lines if not valid_next(l)), None)
    if rule:
        return f"The next state, write symbol or direction is missing in rule:\n{rule}"

    rule = next((l for l in lines if not valid_write(l)), None)
    if rule:
        return f"Invalid write symbol length (> 1) in rule\n{rule}"

    rule = next((l for l in lines if not valid_dir(l)), None)
    if rule:
        return f"Invalid direction in rule:\n{rule}"


if __name__ == "__main__":
    pass
