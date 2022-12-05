from ib110hw.turing.machine import TransitionFunction, Direction, TuringMachine

# Navrhněte deterministický Turinguv stroj T počítající funkci f:
#   {a, b}* → {b, c}* takovou, že pro libovolné w ∈ {a, b} je f(w) slovo,
#   které vznikne nahrazením každého výskytu znaku 'a' slovem 'cc'.
#
# Příklad:
# • f(abba) = ccbbcc
# • f(babbaa) = bccbbcccc
# • f(aaa) = cccccc


def turing_machine() -> TuringMachine:
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

    return TuringMachine(
        states={"init", "space", "writeA", "writeB", "findA", "back"},
        acc_states={"finish"},
        rej_states=set(),
        initial_state="init",
        input_alphabet={"a", "b", "c"},
        transition_function=fn)


if __name__ == "__main__":
    machine = turing_machine()
    machine.tape.write(">aba")

    print(machine.simulate(delay=.2), "\n")
