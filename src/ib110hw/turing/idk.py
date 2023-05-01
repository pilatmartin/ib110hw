from .dtm import DTM
from .tape import Direction

if __name__ == "__main__":
    transitions = {
        "init": {
            ">": ("findA", ">", Direction.RIGHT),
        },
        "findA": {
            "a": ("findB", "a", Direction.RIGHT),
            "b": ("findA", "b", Direction.RIGHT),
            "c": ("findA", "c", Direction.RIGHT),
        },
        "findB": {
            "a": ("findB", "a", Direction.RIGHT),
            "b": ("markC", "b", Direction.RIGHT),
            "c": ("findA", "c", Direction.RIGHT),
        },
        "markC": {
            "a": ("shiftA", "X", Direction.RIGHT),
            "b": ("shiftB", "X", Direction.RIGHT),
            "c": ("shiftC", "X", Direction.RIGHT),
            "": ("findA", "c", Direction.RIGHT),
        },
        "shiftA": {
            "a": ("shiftA", "a", Direction.RIGHT),
            "b": ("shiftB", "a", Direction.RIGHT),
            "c": ("shiftC", "a", Direction.RIGHT),
            "": ("goBack", "a", Direction.LEFT),
        },
        "shiftB": {
            "a": ("shiftA", "b", Direction.RIGHT),
            "b": ("shiftB", "b", Direction.RIGHT),
            "c": ("shiftC", "b", Direction.RIGHT),
            "": ("goBack", "b", Direction.LEFT),
        },
        "shiftC": {
            "a": ("shiftA", "c", Direction.RIGHT),
            "b": ("shiftB", "c", Direction.RIGHT),
            "c": ("shiftC", "c", Direction.RIGHT),
            "": ("goBack", "c", Direction.LEFT),
        },
        "goBack": {
            "a": ("goBack", "a", Direction.LEFT),
            "b": ("goBack", "b", Direction.LEFT),
            "c": ("goBack", "c", Direction.LEFT),
            "X": ("findA", "c", Direction.RIGHT),
        },
    }

    machine = DTM(
        states={*transitions.keys()},
        input_alphabet={"a", "b", "c"},
        transitions=transitions,
    )

    machine.write_to_tape("abba")
    machine.simulate(step_by_step=True)
